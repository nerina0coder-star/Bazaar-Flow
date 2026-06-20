from app.repositories.user_repository import UserRepository
from app.repositories.participant_repository import ParticipantRepository
from app.repositories.chamber_repository import ChamberRepository

def repositories():
    return {
        "ChamberRepository": ChamberRepository,
        "UserRepository": UserRepository,
        "ParticipantRepository": ParticipantRepository,
    }