from app.extensions import db
from app.models.chamber import Chamber


class ChamberRepository:

    @staticmethod
    def find_chamber_by_id(chamber_id: int) -> Chamber:
        return Chamber.query.get(chamber_id)

    @staticmethod
    def find_chamber_by_name(name: str) -> Chamber:
        return Chamber.query.filter_by(name=name).first()

    @staticmethod
    def create_chamber(name) -> Chamber:
        chamber = Chamber(name=name)
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