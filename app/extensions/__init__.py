import datetime
from zoneinfo import available_timezones

from flask import request, g, current_app, session, Response
from flask_babel import Babel
from flask_babel_js import BabelJS
from flask_cors import CORS
from flask_hcaptcha import hCaptcha
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, current_user
from flask_paranoid import Paranoid
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf import CSRFProtect

from .Redis import Redis

db = SQLAlchemy()

csrf = CSRFProtect()
captcha = hCaptcha()
talisman = Talisman()

socket_io = SocketIO(async_mode="gevent", logger=True, manage_session=False,
                     engineio_logger=True, max_http_buffer_size=5 * 1024 * 1024)

cors = CORS(supports_credentials=True)
limiter = Limiter(key_func=lambda: get_remote_address(),
                  default_limits=["500 per day;100 per hour;50 per minute;10 per second"],
                  storage_uri="redis://localhost:6379")

login_manager = LoginManager()
login_manager.login_view = "auth.login"

paranoid = Paranoid()
paranoid.redirect_view = "/"


redis = Redis(less_calls=True)

def get_locale():
    user = current_user if current_user.is_authenticated else None
    if user is None:
        return request.accept_languages.best_match(['en', 'fa']) or current_app.config["BABEL_DEFAULT_LOCALE"]
    return user.lang if user.lang in current_app.config["SUPPORTED_LOCALES"] else current_app.config[
        "BABEL_DEFAULT_LOCALE"]


def get_timezone():
    user = getattr(g, 'user', None)
    if user is None:
        return current_app.config["BABEL_DEFAULT_TIMEZONE"]
    return user.timezone if user.timezone in available_timezones() else current_app.config["BABEL_DEFAULT_TIMEZONE"]


babel = Babel()
babeljs = BabelJS()

utc = lambda: datetime.datetime.now(datetime.UTC)
