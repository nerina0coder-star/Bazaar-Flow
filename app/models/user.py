import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(300))
    username = db.Column(db.String(64))

    time_joined = db.Column(db.DateTime, default=datetime.datetime.now)

    last_seen = db.Column(db.DateTime, default=datetime.datetime.now)

    is_active = db.Column(db.Boolean, default=True)

    description = db.Column(db.String(200))

    credits = db.Column(db.Integer, default=0, nullable=False)

    is_public = db.Column(db.Boolean, default=False)

    lang = db.Column(db.String(120), default='fa')
    timezone = db.Column(db.String(120), default='Asia/Tehran')

    # One-to-many

    messages = db.relationship('Message', backref='author', lazy='dynamic')
    items = db.relationship('Item', backref='author', lazy='dynamic')

    # Many-to-many

    participants = db.relationship('Participant', back_populates='user', lazy='dynamic')
    banned_from = db.relationship('BannedUser', back_populates='user', lazy='dynamic')

    chambers = db.relationship(
        'Chamber',
        secondary='participant',  # table name
        primaryjoin='User.id == Participant.user_id',
        secondaryjoin='Participant.chamber_id == Chamber.id',
        viewonly=True,
        lazy='dynamic'
    )

    banned = db.relationship(
        'Chamber',
        secondary='banned_user',
        primaryjoin='User.id == BannedUser.user_id',
        secondaryjoin='BannedUser.chamber_id == Chamber.id',
        viewonly=True,
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_online(self):
        if datetime.datetime.now(datetime.UTC).replace(tzinfo=None) - self.last_seen < datetime.timedelta(minutes=5):
            return True
        return False

    def __repr__(self):
        return f'<User {self.email}>'
