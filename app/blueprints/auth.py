from email_validator import validate_email
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_babel import gettext as _
from flask_login import login_user, logout_user, login_required
from flask_wtf.csrf import validate_csrf, CSRFError
from urllib.parse import urlparse

from app.extensions import captcha
from app.forms import RegistrationForm, LoginForm
from app.services.user_service import UserService

auth_bp = Blueprint('auth', __name__)


def _is_safe_redirect_target(target):
    if not target:
        return False
    normalized_target = target.replace('\\', '')
    parsed_target = urlparse(normalized_target)
    return not parsed_target.netloc and not parsed_target.scheme


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():

        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('auth/login.html', csrfError=True, form=form)

        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')

        if current_app.config.get('use_captcha') and not captcha.verify():
            return render_template('auth/login.html', CaptchaError=True, form=form)

        user = UserService.authenticate(username, email, password)

        if user:
            login_user(user)
            next_page = request.args.get('next')
            if not _is_safe_redirect_target(next_page):
                next_page = None
            return redirect(next_page or url_for('profile.dashboard'))
        else:
            return render_template('auth/login.html',
                                   customMessage=_("ولی یا رمزت یا ایمیلت یا هم نام کاربریت اشتباهه..."),
                                   form=form
                                   )

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('auth/register.html', csrfError=True, form=form)
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        terms_accepted = request.form.get('termsCheck') == 'on'

        if not terms_accepted or terms_accepted is None:
            return render_template("auth/register.html",
                                   userError=_("به دلیل موافقت نکردن با قوانین و مقررات شکست خورد"),
                                   form=form)

        try:
            validate_email(email)
            UserService.register_user(email, password, username)
            return redirect(url_for('auth.login'))
        except ValueError:
            return render_template('auth/register.html', form=form,
                                   userError=_("شکست خورد، این ایمیل قبلا ثبت شده است"))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':

        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('auth/logout.html', csrfError=True)

        logout_user()
        return redirect(url_for('home'))
    return render_template('auth/logout.html')
