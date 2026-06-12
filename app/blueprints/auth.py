from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from flask_wtf.csrf import validate_csrf, CSRFError

from app.services.user_service import UserService
from app.extensions import captcha
from email_validator import validate_email, EmailNotValidError

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('auth/login.html', csrfError=True)

        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')

        if (email is None or password is None) or \
                (email == '' or password == ''):
            return render_template('auth/login.html', customMessage=
            "همم... به نظر می‌رسه ایمیل یا پسوردت خالیه...")

        if not captcha.verify():
            return render_template('auth/login.html', CaptchaError=True)

        user = UserService.authenticate(username, email, password)

        if user:
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('profile.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html', customMessage=
            "ولی یا رمزت یا ایمیلت یا هم نام کاربریت اشتباهه..."
                                   )

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('auth/register.html', csrfError=True)

        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        terms_accepted = request.form.get('termsCheck', type=bool)

        if (email is None or password is None or username is None or terms_accepted is None) or \
                (email == '' or password == '' or username == '' or terms_accepted == ''):
            return render_template("auth/register.html", passwordError=False,
                                   userError="موفق نبود٬ به نظر می‌رسد یک یا چند مورد از گزینه ها خالی است")

        if not terms_accepted or terms_accepted is None:
            return render_template("auth/register.html", passwordError=False,
                                   userError="به دلیل موافقط نکردن با قوانین و مقررات شکست خورد")

        if password != request.form.get('confirmPassword'):
            return render_template("auth/register.html", passwordError=False,
                                   userError="شکست خورد٬ رمز عبور با رمز عبور تاییدی مطابقت ندارد")

        if len(username) > 63:
            return render_template("auth/register.html", passwordError=False,
                                   userError='شکست خورد٬ نام کاربری نباید بیشتر از ۶۳ کاراکتر باشد')
        if len(email) > 119:
            return render_template('auth/register.html', passwordError=False,
                                   userError='شکست خورد٬ طول ایمیل نباید بیشتر از ۱۱۹ کاراکتر باشد')

        try:
            validate_email(email)
            UserService.register_user(email, password, username)
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except EmailNotValidError:
            return render_template('auth/register.html', passwordError=True,
                                   userError="به دلیل غلت بودن ایمیل شکست خورد")
        except ValueError:
            if len(password) < 8:
                return render_template('auth/register.html', passwordError=True)
            else:
                return render_template('auth/register.html', passwordError=False,
                                       userError="شکست خورد٬ این ایمیل قبلا ثبت شده است")
    return render_template('auth/register.html')


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':

        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            return render_template('auth/logout.html', csrfError=True)

        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))
    return render_template('auth/logout.html')
