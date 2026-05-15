from app.extensions import db
from .message import Message
from .participant import Participant

class Chamber(db.Model):
    __tablename__ = 'chamber'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.String(50), nullable=False)

    entrance_code = db.Column(db.String(100), nullable=False)

    # many-to-many
    participants = db.relationship('Participant', back_populates='chamber', lazy='dynamic')

    users = db.relationship(
        'User',
        secondary='participants',
        primaryjoin='Chamber.id == Participant.chamber_id',
        secondaryjoin='Participant.user_id == User.id',
        viewonly=True,
        lazy='dynamic'
    )

    # one-to-many

    messages = db.relationship('Message', back_populates='chamber', lazy='dynamic')

    async def get_last_message(self):
        return self.messages.query.order_by(Message.timestamp.desc()).first()