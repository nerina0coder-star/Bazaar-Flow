from flask import Blueprint, render_template, request, redirect, url_for
from flask_babel import gettext as _
from flask_login import login_required, current_user
from flask_wtf.csrf import validate_csrf, CSRFError

from app.extensions import limiter
from app.forms import EditProfileForm
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
    form = EditProfileForm()
    form.description.data = current_user.description
    form.language.data = current_user.lang
    form.timezone.data = current_user.timezone

    if request.method == 'POST':

        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('profile/edit.html', csrfError=True)

        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        description = request.form.get('description').strip()
        description = description if description else None

        visible = request.form.get('is_public') == 'y'

        lang = request.form.get('language')
        timezone = request.form.get('timezone')

        username = request.form.get('username')
        password = request.form.get('password')

        if not current_user.check_password(password) and new_password:
            return render_template('profile/edit.html', custom_message=_('شکست خورد، رمز عبور صحیح ‌نمی‌باشد'))

        if visible:
            tc = request.form.get("terms_accepted") == 'on'
            pp = request.form.get("privacy_accepted") == 'on'
            if not tc or not pp:
                return render_template('profile/edit.html', form=form,
                                       custom_message=_('شکست خورد، لطفا برای دیده شدن در صفحه '
                                                        'اصلی شرایط و ضوابط را به همراه سیاست '
                                                        'حفظ حریم خصوصی تایید کنید.'))
        UserService.update_profile(current_user.id, username, new_password, description, visible, lang, timezone)
        return redirect(url_for('profile.dashboard'))

    return render_template('profile/edit.html', user=current_user, form=form)
