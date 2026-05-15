from app import db
from app.models.participant import Participant
from app.models.user import User
from app.models.chamber import Chamber
from app.repositories.chamber_repository import ChamberRepository
from app.repositories.user_repository import UserRepository


class ParticipantRepository:

    @staticmethod
    def add_to_chamber(user_id: int | list[int], chamber_id: int | list[int], role: str | list[str] = 'member'):

        if isinstance(chamber_id, int):
            chamber_id = [chamber_id]
        if isinstance(user_id, int):
            user_id = [user_id]
        if isinstance(role, str):
            role = [role]

        if len(user_id) > len(role):
            role.extend(['member' for _ in range(len(user_id) - len(role))])
        elif len(chamber_id) < len(role):
            return None

        parts = []
        for uid in range(len(user_id)):
            if UserRepository.find_by_id(user_id[uid]) is None:
                return None
            for cid in chamber_id:

                if ChamberRepository.find_by_id(cid) is None:
                    return None
                exists = Participant.query.filter_by(chamber_id = cid, user_id = user_id[uid]).one_or_none()
                if exists:
                    continue

                part = Participant(chamber_id=cid, user_id=user_id[uid], role=role[uid])
                parts.append(part)
        db.session.add_all(parts)
        db.session.commit()
        return len(parts)