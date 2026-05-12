from app.extensions import db
from .participants import participants

class Chamber(db.Model):
    __tablename__ = 'chamber'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # many-to-many

    users = db.relationship('User', secondary=participants, back_populates='chambers', lazy='dynamic')

    # one-to-many

    messages = db.relationship('Message', back_populates='chamber', lazy='dynamic')