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
    def find_by_id(user_id):
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