from app.extensions import db

class BannedUser(db.Model):
    __tablename__ = 'banned_user'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    chamber_id = db.Column(db.Integer, db.ForeignKey('chamber.id'), primary_key=True)

    user = db.relationship('User', back_populates='banned_chambers')
    chamber = db.relationship('Chamber', back_populates='banned_users')