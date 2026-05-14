from app.extensions import db

# for many-to-many relationship of users and chambers
class Participant(db.Model):
    __tablename__ = 'participants'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    chamber_id = db.Column(db.Integer, db.ForeignKey('chamber.id'), primary_key=True)

    role = db.Column(db.String(20), nullable=False, default='member')

    # Relationships back to User and Chamber (optional, but useful)
    user = db.relationship('User', back_populates='participants')
    chamber = db.relationship('Chamber', back_populates='participants')