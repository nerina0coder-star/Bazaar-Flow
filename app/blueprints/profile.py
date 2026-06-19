from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf.csrf import validate_csrf, CSRFError

from app import limiter
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
            return render_template('profile/edit.html', custom_message='شکست خورد٬ به نظر میرسد نام‌کاربری یا رمزعبور وارد نشده')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        description = request.form.get('description').strip()
        description = description if description else None
        
        visible = request.form.get('is_public') == 'on'

        username = request.form['username']
        password = request.form['password']

        if not current_user.check_password(password):
            return render_template('profile/edit.html', custom_message='شکست خورد٬ رمزعبور صحیح ‌نمی‌باشد')
        if new_password != confirm_password:
            return render_template('profile/edit.html', passwordError = True)
        if description is not None and len(description) > 20:
            return render_template('profile/edit.html', custom_message='شکست خورد٬ طول توضیحات نباید بیش از ۲۰۰ کاراکتر شود')
        if visible:
            tc = request.form.get("terms_accepted") == 'on'
            privacy_policy = request.form.get("privacy_accepted") == 'on'
            if not tc or not privacy_policy:
                return render_template('profile/edit.html', custom_message='شکست خورد٬ لطفا برای دیده شدن در صفحه اصلی شرایط و ضوابت را به همراه سیاست حفظ حریم خصوصی تایید کنید.')
        
        try:
            UserService.update_profile(current_user.id, username, new_password, description, visible)
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile.dashboard'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('profile/edit.html', user=current_user)
