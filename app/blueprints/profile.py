from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf.csrf import validate_csrf, CSRFError
from flask_babel import gettext as _

from app.extensions import limiter
from app.services.user_service import UserService

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/dashboard')
@login_required
@limiter.limit("5000 per hour")
def dashboard():
    return render_template('profile/memory.html')


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':


        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('profile/edit.html', csrfError=True)

        if request.form.get('username') is None or request.form.get('password') is None:
            return render_template('profile/edit.html', custom_message=_('شکست خورد، به نظر می‌رسد نام کاربری یا رمز '
                                                                         'عبور وارد نشده'))
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        description = request.form.get('description').strip()
        description = description if description else None
        
        visible = request.form.get('is_public') == 'on'

        lang = request.form.get('language')
        timezone = request.form.get('timezone')

        username = request.form.get('username')
        password = request.form.get('password')

        if username is None or not username or password is None or not password:
            return render_template('profile/edit.html', custom_message=_('شکست خورد، نام کاربری یا رمز عبور خالی است'))
        if lang is None or not lang or timezone is None or not timezone:
            return render_template('profile/edit.html', custom_message=_('شکست خورد، زبان یا منطقه زمانی خالی است'))
        if lang not in ('fa', 'en') or timezone not in ('Asia/Tehran', 'US/Eastern'):
            return render_template('profile/edit.html', cutom_message=_('شکست خورد، زبان یا منطفه زمانی پشتیبانی نشده '
                                                                        'وارد شد'))

        #if not current_user.check_password(password):
        #    return render_template('profile/edit.html', custom_message=_('شکست خورد، رمز عبور صحیح ‌نمی‌باشد'))
        if new_password != confirm_password:
            return render_template('profile/edit.html', passwordError = True)
        if description is not None and len(description) > 20:
            return render_template('profile/edit.html', custom_message=_('شکست خورد، طول توضیحات نباید بیش از ۲۰۰ '
                                                                         'کاراکتر شود'))
        if visible:
            tc = request.form.get("terms_accepted") == 'on'
            privacy_policy = request.form.get("privacy_accepted") == 'on'
            if not tc or not privacy_policy:
                return render_template('profile/edit.html', custom_message=_('شکست خورد، لطفا برای دیده شدن در صفحه '
                                                                             'اصلی شرایط و ضوابط را به همراه سیاست '
                                                                             'حفظ حریم خصوصی تایید کنید.'))
        
        try:
            UserService.update_profile(current_user.id, username, new_password, description, visible, lang, timezone)
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile.dashboard'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('profile/edit.html', user=current_user)
