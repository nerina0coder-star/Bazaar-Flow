from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.services.user_service import UserService

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('profile/memory.html')


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        if request.form.get('username') is None or request.form.get('password') is None:
            return render_template('profile/edit.html', custom_message='شکست خورد٬ به نظر میرسد نام‌کاربری یا رمزعبور وارد نشده')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        username = request.form['username']
        password = request.form['password']

        if not current_user.check_password(password):
            return render_template('profile/edit.html', custom_message='شکست خورد٬ رمزعبور صحیح نمی‌باشد')
        if new_password != confirm_password:
            return render_template('profile/edit.html', passwordError = True)

        try:
            UserService.update_profile(current_user.id, username, new_password)
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile.dashboard'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('profile/edit.html', user=current_user)