from app import db
from app.models.banned_user import BannedUser


class BannedUserRepository:

    @staticmethod
    def find_by_ids(chamber_id: int, user_id: int) -> BannedUser:
        return BannedUser.query.filter_by(chamber_id=chamber_id, user_id=user_id).first()

    @staticmethod
    def ban_user(chamber_id: int, user_id: int) -> BannedUser:
        ban = BannedUser(chamber_id=chamber_id, user_id=user_id)
        db.session.add(ban)
        db.session.commit()
        return ban

    @staticmethod
    def is_banned(chamber_id: int, user_id: int) -> bool:
        is_banned = BannedUserRepository.find_by_ids(chamber_id, user_id)
        return is_banned is not None