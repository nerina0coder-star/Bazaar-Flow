from app.models.participant import Participant
from app.models.user import User
from app.extensions import db


class UserRepository:
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_id(user_id) -> User | None:
        return User.query.get(user_id)

    @staticmethod
    def create(email, password, username):
        user = User(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user, **kwargs):
        for key, value in kwargs.items():
            if hasattr(user, key) and key != 'id':
                setattr(user, key, value)
        db.session.commit()

    @staticmethod
    def is_owner(chamber_id, user_id):
        owner = Participant.query.filter_by(chamber_id=chamber_id, user_id=user_id, role='owner').first()
        return owner is not None