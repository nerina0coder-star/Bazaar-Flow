from app.extensions import db
from app.models.chamber import Chamber
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
    def create_chamber(name: str, entrance_code: str) -> Chamber:
        chamber = Chamber(name=name, entrance_code=entrance_code)
        db.session.add(chamber)
        db.session.commit()
        return chamber

    @staticmethod
    def delete_chamber(chamber_id: int) -> None:
        chamber = Chamber.query.get(chamber_id)
        db.session.delete(chamber)
        db.session.commit()

    @staticmethod
    def edit_chamber(chamber_id: int, name: str) -> Chamber:
        chamber = Chamber.query.get(chamber_id)
        chamber.name = name
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