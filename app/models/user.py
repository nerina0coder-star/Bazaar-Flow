from app.extensions import db, login_manager
from flask_login import UserMixin
from .participants import participants

from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, default=True)

    credits = db.Column(db.Integer, default=0, nullable=False)

    # On-to-many

    messages = db.relationship('Message', backref='author', lazy='dynamic')
    items = db.relationship('Item', backref='author', lazy='dynamic')

    # Many-to-many

    chambers = db.relationship('Chamber', secondary=participants ,back_populates='users', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'