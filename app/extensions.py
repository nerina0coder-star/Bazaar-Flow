from zoneinfo import ZoneInfo

from flask_cors import CORS
from flask_hcaptcha import hCaptcha
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_paranoid import Paranoid

db = SQLAlchemy()
socket_io = SocketIO(async_mode="gevent", logger=True, engineio_logger=True, max_http_buffer_size=5 * 1024 * 1024)
csrf = CSRFProtect()
captcha = hCaptcha()
talisman = Talisman()
cors = CORS(supports_credentials=True)
limiter = Limiter(key_func=lambda: get_remote_address(),
                  default_limits=["500 per day;100 per hour;50 per minute;10 per second"],
                  storage_uri="redis://localhost:6379")

login_manager = LoginManager()
login_manager.login_view = "auth.login"

paranoid = Paranoid()
paranoid.redirect_view = "/"

iran_tz = ZoneInfo('Asia/Tehran')
