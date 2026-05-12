from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.services.user_service import UserService

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('profile/dashboard.html', user=current_user)
@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        try:
            UserService.update_profile(current_user.id, first_name, last_name)
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile.dashboard'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('profile/edit.html', user=current_user)