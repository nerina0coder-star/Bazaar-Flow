from app.extensions import db
from app.models.chamber import Chamber
from app.models.message import Message
from app.models.participant import Participant
from app.repositories.user_repository import UserRepository


class ChamberRepository:

    @staticmethod
    def find_by_id(chamber_id: int) -> Chamber | None:
        return Chamber.query.get(chamber_id)

    @staticmethod
    def find_by_name(name: str) -> Chamber:
        return Chamber.query.filter_by(name=name).first()

    @staticmethod
    def create_chamber(name: str, entrance_code: str, description: str) -> Chamber:
        chamber = Chamber(name=name, entrance_code=entrance_code, description=description)
        db.session.add(chamber)
        db.session.commit()
        return chamber

    @staticmethod
    def delete_chamber(chamber_id: int) -> None:
        chamber = Chamber.query.get(chamber_id)
        db.session.delete(chamber)
        db.session.commit()

    @staticmethod
    def edit_chamber(chamber_id: int,
                     name: str,
                     entrance_code: str,
                     description: str,
                     is_primary: bool|None = None,
                     is_public: bool|None = None) -> Chamber:
        chamber = Chamber.query.get(chamber_id)
        chamber.name = name
        chamber.entrance_code = entrance_code
        chamber.description = description
        if is_public is not None:
            chamber.is_public = is_public
        if is_primary is not None:
            Participant.query.filter_by(chamber_id=chamber.id).first().is_primary = is_primary
        db.session.commit()
        return chamber

    @staticmethod
    def remove_user_from(chamber_id: int, user_id: int) -> None:
        chamber = Chamber.query.get(chamber_id)
        chamber.users.remove(user_id)
        db.session.commit()

    @staticmethod
    def get_owner(chamber_id: int) -> Chamber | None:
        owner = Participant.query.filter_by(chamber_id=chamber_id, role='owner').first()
        return owner if owner else None

    @staticmethod
    def add_user(chamber_id: int, user_id: int) -> Chamber | None:
        chamber = Chamber.query.get(chamber_id)
        user = UserRepository.find_by_id(user_id)
        chamber.users.append(user)
        db.session.commit()
        return chamber
    @staticmethod
    def messages(chamber_id: int, limit: int = 50):
        return ChamberRepository.find_by_id(chamber_id).messages.order_by(Message.timestamp.desc()).limit(limit).all()
