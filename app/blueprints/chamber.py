from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from flask_login import login_required, current_user
from flask_socketio import emit, join_room, leave_room

from app.models import Participant
from app.repositories.user_repository import UserRepository
from app.services.chamber_service import ChamberService
from app.repositories.participant_repository import ParticipantRepository
from app.repositories.chamber_repository import ChamberRepository
from app.repositories.message_repository import MessageRepository
from app.extensions import socket_io, db, iran_tz

chamber_bp = Blueprint('chamber', __name__)


@chamber_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('chamber/dashboard.html')

@chamber_bp.route('/join', methods=['GET', 'POST'])
def join():

    if request.method == 'POST':
        try:
            code = request.form.get('code')
        except Exception:
            return abort(400)

        if not code or code is None:
            return abort(400)

        if code.count("|") == 0:
            return render_template('chamber/join.html', message= 'شکست خورد٬ کد واردشده اشتباه است')

        # id|entrance code


        chamber_id = int(code[0:code.rindex('|')])
        chamber_entrance_code = code[code.index('|') + 1:]



        chamber = ChamberRepository.find_by_id(chamber_id)
        if chamber is None:
            return render_template('chamber/join.html', message='شکست خورد٬ تالار یافت نشد')

        if chamber.entrance_code != chamber_entrance_code:
            return render_template('chamber/join.html', message='شکست خورد٬ رمز ورود اشتباه است')

        ParticipantRepository.add_to_chamber(current_user.id, chamber_id)

        return redirect(url_for('chamber.chamber', data=chamber_id))




    return render_template('chamber/join.html')

@chamber_bp.route('/chambers/<int:data>')
@login_required
def chamber(data):
    chamber = ChamberRepository.find_by_id(data)

    if chamber is None:
        return abort(400)

    if chamber not in current_user.chambers:
        return abort(403)

    session['chamber'] = chamber.id


    if UserRepository.is_owner(chamber.id, current_user.id):
        return render_template('chamber/chamber.html', chamber_id=chamber.id, copyEntryCode = True)
    else:
        return render_template('chamber/chamber.html', chamber_id=chamber.id)

@chamber_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():

    if request.method == 'POST':
        if request.form.get('name') is None or request.form.get('entrance_code') is None:
            return render_template('chamber/create.html')

        name = request.form.get('name')
        entrance_code = request.form.get('entrance_code')

        if len(entrance_code) > 99:
            return render_template('chamber/create.html', custom_message='شکست خورد٬ کد ورود نباید بیش از ۹۹ کاراکتر باشد.')
        if len(name) > 99:
            return render_template('chamber/create.html', custom_message='شکست خورد٬ نام تالار نباید بیش از ۹۹ کاراکتر باشد')

        try:
            chamber = ChamberService.create_chamber(name, entrance_code)
        except Exception:
            return render_template('chamber/create.html', custom_message="شکست خورد٬ این تالار قبلا ساخته شده")

        ParticipantRepository.add_to_chamber(user_id=current_user.id, chamber_id=chamber.id, role='owner')

        return redirect(url_for('chamber.chamber', data=chamber.id))

    return render_template('chamber/create.html')

@socket_io.on('message_from_client')
@login_required
def handle_msg(data):

    try:
        chamber = ChamberRepository.find_by_id(session['chamber'])
        message = data['message']
    except Exception:
        return abort(400)

    if chamber is None:
        return abort(404)
    if chamber not in current_user.chambers:
        return abort(403)
    if message.strip() == '':
        return abort(400)

    message = MessageRepository.create(message, chamber.id, current_user.id)

    hour_timestamp = message.timestamp.astimezone(iran_tz).strftime('%H:%M')
    month_timestamp = message.timestamp.astimezone(iran_tz).strftime('%d %b, ')

    emit('message_from_server', {
        'message': data['message'],
        'author': current_user.username,
        'timehourminute' : hour_timestamp,
        'timemonthday' : month_timestamp
    }, to=str(chamber.id))

    return None

@socket_io.on('get_entrance_code')
def get_code():
    emit('entrance_code', {'code' : f"{session['chamber']}|{ChamberRepository.find_by_id(session['chamber']).entrance_code}"}, to=str(session['chamber']))

@socket_io.on('connect')
@login_required
def handle_joined():

    try:
        ChamberRepository.find_by_id(session['chamber'])
    except Exception:
        return abort(400)

    join_room(str(session['chamber']))
    if ChamberRepository.find_by_id(session['chamber']) is None:
        return abort(404)

    for i in ChamberRepository.find_by_id(session['chamber']).messages:
        content = i.content
        hour_timestamp = i.timestamp.astimezone(iran_tz).strftime('%H:%M')
        month_timestamp = i.timestamp.astimezone(iran_tz).strftime('%d %b, ')
        author = i.author.username

        emit('message_from_server', {
            'message' : content,
            'timehourminute' : hour_timestamp,
            'timemonthday' : month_timestamp,
            'author' : author,
        }, to=str(session['chamber']))


    if ChamberRepository.find_by_id(session['chamber']) not in current_user.chambers:

        ParticipantRepository.add_to_chamber(current_user.id, session['chamber'])
        emit('message_from_server', {
            'message' : f'کاربر {current_user.username} وارد تالار شد',
            'author' : 'سیستم',
            'timehourminute' : datetime.now().strftime('%H:%M'),
            'timemonthday' : datetime.now().strftime('%d %b, ')
        }, to=str(session['chamber']))

@socket_io.on('disconnect')
def handle_left():
    try:
        chamber = ChamberRepository.find_by_id(session['chamber'])
    except Exception:
        return abort(400)

    leave_room(str(chamber.id))