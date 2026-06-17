import datetime
from zoneinfo import ZoneInfo

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_wtf import CSRFProtect
from flask_hcaptcha import hCaptcha
from flask_talisman import Talisman
from flask_cors import CORS

db = SQLAlchemy()
socket_io = SocketIO(async_mode="gevent", logger=True, engineio_logger=True, max_http_buffer_size=5 * 1024 * 1024)
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = "auth.login"
captcha = hCaptcha()
talisman = Talisman()
cors = CORS(supports_credentials=True)

iran_tz = ZoneInfo('Asia/Tehran')
