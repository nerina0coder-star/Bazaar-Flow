from sqlalchemy import or_

from app.extensions import db
from app.models.participant import Participant
from app.models.user import User


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

    @staticmethod
    def get_related(user: User):
        ignoring = {
            'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'am', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'shall', 'should', 'can', 'could', 'may', 'might', 'must',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'its', 'our', 'their', 'this', 'that', 'these', 'those',
            'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'over', 'after'
        }
        pattern = (f'%{j}%' for j in user.description.split() if j.lower() not in ignoring) or None
        if not pattern or pattern == None:
            return None
        pattern = [User.description.ilike(p) for p in pattern]
        return User.query.filter(or_(*pattern), User.id != user.id).filter_by(is_public=True).limit(20).all()
