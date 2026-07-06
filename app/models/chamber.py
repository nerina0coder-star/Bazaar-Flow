from app.extensions import db
from .message import Message


class Chamber(db.Model):
    __tablename__ = 'chamber'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.String(500), nullable=False)

    entrance_code = db.Column(db.String(100), nullable=False)

    is_public = db.Column(db.Boolean, nullable=False, default=False)

    # many-to-many
    participants = db.relationship('Participant', back_populates='chamber', lazy='dynamic')
    banned_users = db.relationship('BannedUser', back_populates='chamber', lazy='dynamic')

    users = db.relationship(
        'User',
        secondary='participant',
        primaryjoin='Chamber.id == Participant.chamber_id',
        secondaryjoin='Participant.user_id == User.id',
        viewonly=True,
        lazy='dynamic'
    )

    banned = db.relationship(
        'User',
        secondary='banned_user',
        primaryjoin='Chamber.id == BannedUser.chamber_id',
        secondaryjoin='BannedUser.user_id == User.id',
        viewonly=True,
        lazy='dynamic'
    )

    # one-to-many

    messages = db.relationship('Message', back_populates='chamber', lazy='dynamic')

    async def get_last_message(self):
        return self.messages.query.order_by(Message.timestamp.desc()).first()
