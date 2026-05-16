import datetime
from zoneinfo import ZoneInfo

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()
socket_io = SocketIO(async_mode="gevent", logger=True, engineio_logger=True)
login_manager = LoginManager()
iran_tz = ZoneInfo('Asia/Tehran')

login_manager.login_view = "auth.login"