from datetime import datetime
from app.extensions import db

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    # Foreign Keys (many-to-one)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chamber_id = db.Column(db.Integer, db.ForeignKey('chamber.id'))

    # Relationships

    chamber = db.relationship('Chamber', back_populates='messages')