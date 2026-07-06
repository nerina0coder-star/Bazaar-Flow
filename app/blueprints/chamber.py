import hmac
import secrets
from hashlib import sha256
from hmac import compare_digest

from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from flask_babel import format_time, format_date, get_locale
from flask_babel import gettext as _
from flask_login import login_required, current_user
from flask_socketio import emit, join_room, leave_room
from flask_wtf.csrf import validate_csrf, CSRFError

from app.extensions import socket_io, limiter, utc, redis as r
from app.forms import CreateChamberForm, EditChamberForm
from app.repositories.banned_user_repository import BannedUserRepository
from app.repositories.chamber_repository import ChamberRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.participant_repository import ParticipantRepository
from app.repositories.user_repository import UserRepository
from app.services.chamber_service import ChamberService

chamber_bp = Blueprint('chamber', __name__)


@chamber_bp.route('/dashboard')
@login_required
@limiter.limit("5000 per hour")
def dashboard():
    chambers = current_user.chambers.all()
    return render_template('chamber/dashboard.html', chambers=chambers, user_repo=UserRepository())


@chamber_bp.route('/chambers/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    if not UserRepository.is_owner(id, current_user.id):
        return abort(400)
    chamber = ChamberRepository.find_by_id(id)

    form = EditChamberForm()

    if request.method == 'GET':
        form.description.data = chamber.description or ''

    if request.method == 'POST' and form.validate_on_submit():

        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('chamber/edit.html', csrfError=True, form=form)

        name = request.form.get('name').strip()
        entrance_code = request.form.get('entrance_code').strip()
        description = request.form.get('description').strip()
        is_primary = request.form.get('is_primary') == 'y'
        is_public = request.form.get('is_public') == 'y'

        ChamberRepository.edit_chamber(id, name, entrance_code, description, is_primary, is_public)

        return redirect(url_for('chamber.dashboard'))

    return render_template('chamber/edit.html', chamber=chamber, form=form)


@chamber_bp.route('/chambers/<int:id>/members')
@login_required
def members(id):
    if not UserRepository.is_owner(id, current_user.id):
        return abort(400)
    chamber = ChamberRepository.find_by_id(id)
    if chamber is None:
        return abort(404)

    return render_template('chamber/members.html', chamber=chamber, partrep=ParticipantRepository())


@chamber_bp.route('/chambers/<int:chamber_id>/members/<int:member_id>', methods=["GET", "POST"])
@login_required
def edit_member(chamber_id, member_id):
    if not UserRepository.is_owner(chamber_id, current_user.id):
        return abort(400)
    part = ParticipantRepository.get(chamber_id=chamber_id, user_id=member_id)
    if part is None:
        return abort(404)

    if request.method == 'POST':

        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('chamber/edit_member.html', csrfError=True)

        ban = request.form.get('ban') == 'on'
        role = request.form.get('role')

        part = ParticipantRepository.get(member_id, chamber_id)

        if ban:
            ParticipantRepository.remove(part)
            BannedUserRepository.ban_user(chamber_id, member_id)
            return redirect(url_for('chamber.dashboard'))
        else:
            # if role != part.role:
            #    part.role = role
            return redirect(url_for('chamber.dashboard'))

    user = UserRepository.find_by_id(member_id)
    chamber = ChamberRepository.find_by_id(chamber_id)

    joined = format_date(user.time_joined, 'medium')

    return render_template('chamber/edit_member.html', chamber=chamber, user=user, joined=joined,
                           role=ParticipantRepository.get(member_id, chamber_id).role)


@chamber_bp.route('/join', methods=['GET', 'POST'])
@login_required
def join():
    if request.method == 'POST':

        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('chamber/join.html', csrfError=True)

        try:
            code = request.form['code']
        except KeyError:
            return abort(400)

        if not code or code is None:
            return abort(400)

        if code.count("|") == 0:
            return render_template('chamber/join.html', message=_('شکست خورد، کد واردشده اشتباه است'))

        # id|entrance code

        chamber_id = int(code[0:code.rindex('|')])
        chamber_entrance_code = code[code.index('|') + 1:]

        chamber = ChamberRepository.find_by_id(chamber_id)
        if chamber is None:
            return render_template('chamber/join.html', message=_('شکست خورد، تالار یافت نشد'))

        if not hmac.compare_digest(chamber.entrance_code, chamber_entrance_code):
            return render_template('chamber/join.html', message=_('شکست خورد، رمز ورود اشتباه است'))

        if BannedUserRepository.is_banned(chamber_id, current_user.id):
            return render_template('chamber/join.html', message=_('شکست خورد، شما را از این تالار مسدود کرده‌اند'))

        just_joined = ParticipantRepository.add_to_chamber(current_user.id, chamber_id) != 0
        if just_joined:
            session['just_joined'] = True

        return redirect(url_for('chamber.chamber', id=chamber_id))

    return render_template('chamber/join.html')


@chamber_bp.route('/chambers/<int:id>')
@login_required
@limiter.limit("5000 per hour")
def chamber(id):
    chamber = ChamberRepository.find_by_id(id)

    if chamber is None:
        return abort(400)

    if chamber not in current_user.chambers:
        return abort(403)

    session['chamber'] = chamber.id
    session['token'] = secrets.token_urlsafe(64)
    raw_vertoken = secrets.token_urlsafe(64)
    session['vertoken'] = sha256(raw_vertoken.encode('utf-8')).hexdigest()

    print("In chamber!")

    if UserRepository.is_owner(chamber.id, current_user.id):
        return render_template('chamber/chamber.html', chamber_id=chamber.id, copyEntryCode=True,
                               token=session['token'], vertoken=raw_vertoken)
    else:
        return render_template('chamber/chamber.html', chamber_id=chamber.id, token=session['token'],
                               vertoken=raw_vertoken)


@chamber_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateChamberForm()

    if request.method == 'POST' and form.validate_on_submit():

        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('chamber/create.html', csrfError=True, form=form)

        name = request.form.get('name').strip()
        entrance_code = request.form.get('entrance_code').strip()
        description = request.form.get('description').strip()
        chamber = ChamberService.create_chamber(name, entrance_code, description)

        ParticipantRepository.add_to_chamber(user_id=current_user.id, chamber_id=chamber.id, role='owner')

        return redirect(url_for('chamber.chamber', id=chamber.id))

    return render_template('chamber/create.html', form=form)


@socket_io.on('message_from_client')
@login_required
def handle_msg(data):
    try:
        chamber = ChamberRepository.find_by_id(session['chamber'])
        message = data['message']
    except KeyError:
        return abort(400)

    if chamber is None:
        return abort(404)
    if chamber not in current_user.chambers:
        return abort(403)
    if message.strip() == '':
        return abort(400)

    # ---
    message = MessageRepository.create(message, chamber.id, current_user.id)

    hour_timestamp = format_time(message.timestamp, 'medium')
    month_timestamp = format_date(message.timestamp, 'dd MMM, ')
    # ---

    messages_count = r[str(current_user.id) + '_messages']
    if messages_count is None:
        r.set(str(current_user.id) + '_messages', str(0), expire=1 * 60 * 60)
    elif messages_count > 1 * 60 * 60:
        emit('message_from_server', {
            'message': _("شما بیشتر از حد مجاز پیام ارسال کرده اید."),
            'author': _('سیستم'),
            'timehourminute': hour_timestamp,
            'timemonthday': month_timestamp,
            'reverse_time': True if str(get_locale()) == 'fa' else False,
            'token': ''
        })

    emit('message_from_server', {
        'message': data['message'],
        'author': current_user.username,
        'timehourminute': hour_timestamp,
        'timemonthday': month_timestamp,
        'reverse_time': True if str(get_locale()) == 'fa' else False,
        'token': session['token']
    }, room=str(chamber.id))

    r(str(current_user.id) + '_messages') + 1

    return None


@socket_io.on('get_entrance_code')
@login_required
def get_code():
    if UserRepository.is_owner(session['chamber'], current_user.id):
        emit('entrance_code',
             {'code': f"{session['chamber']}|{ChamberRepository.find_by_id(session['chamber']).entrance_code}"},
             to=request.sid)


@socket_io.on('client_ask_more')
@login_required
def return_more(data):
    if data.get('after') is None:
        return abort(400)
    after = data['after']
    messages = MessageRepository.get(after=after, chamber=ChamberRepository.find_by_id(session['chamber']))
    if not messages:
        socket_io.emit('server_send_more', {
            'nomore': True
        })
    else:
        for i in messages:
            author = UserRepository.find_by_id(i.user_id)
            socket_io.emit('server_send_more', {
                'islast': False if i != messages[-1] else True,
                'message': i.content,
                'author': author.username,
                'timehourminute': format_time(i.timestamp, 'short'),
                'timemonthday': format_date(i.timestamp, 'dd MMM, '),
                'nomore': False,
                'reverse_time': True if str(get_locale()) == 'fa' else False,
                'token': None if current_user.id != author.id else session['token']
            }, to=request.sid)


@socket_io.on('connect')
def handle_joined(auth):
    if not auth or not compare_digest(sha256(auth['token'].encode('utf-8')).hexdigest(), session.get('vertoken')):
        return abort(403)
    else:
        session.pop('vertoken', None)

    try:
        chamber = ChamberRepository.find_by_id(session['chamber'])
    except KeyError:
        return abort(400)

    join_room(str(session['chamber']))
    if chamber is None:
        return abort(404)

    for i in MessageRepository.get(chamber=chamber)[::-1]:
        content = i.content
        hour_timestamp = format_time(i.timestamp, 'short')
        month_timestamp = format_date(i.timestamp, 'dd MMM, ')
        author = i.author.username
        is_author = i.author == current_user

        emit('message_from_server', {
            'message': content,
            'timehourminute': hour_timestamp,
            'timemonthday': month_timestamp,
            'author': author,
            'reverse_time': True if str(get_locale()) == 'fa' else False,
            'token': '' if not is_author else session['token']
        }, to=request.sid)

    if session.get('just_joined') is not None:
        emit('message_from_server', {
            'message': _(f'کاربر %(username)s وارد تالار شد', username=current_user.username),
            'author': _('سیستم'),
            'timehourminute': format_time(utc(), 'short'),
            'timemonthday': format_date(utc(), 'dd MMM, '),
            'reverse_time': True if str(get_locale()) == 'fa' else False,
        }, room=str(session['chamber']))
    session.pop('just_joined', None)


@socket_io.on('disconnect')
@login_required
def handle_left():
    try:
        chamber = ChamberRepository.find_by_id(session['chamber'])
    except KeyError:
        return abort(400)

    leave_room(str(chamber.id))
