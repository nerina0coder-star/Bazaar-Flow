import datetime
from zoneinfo import ZoneInfo

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_wtf import CSRFProtect
from flask_hcaptcha import hCaptcha

db = SQLAlchemy()
socket_io = SocketIO(async_mode="gevent", logger=True, engineio_logger=True)
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = "auth.login"
captcha = hCaptcha()

iran_tz = ZoneInfo('Asia/Tehran')
