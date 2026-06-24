import flask_babel

from app.repositories.user_repository import UserRepository
from app.repositories.participant_repository import ParticipantRepository
from app.repositories.chamber_repository import ChamberRepository

def repositories():
    return {
        "ChamberRepository": ChamberRepository,
        "UserRepository": UserRepository,
        "ParticipantRepository": ParticipantRepository,
    }
def locale():
    return {
        'current_locale' : flask_babel.get_locale,
        'current_timezone' : flask_babel.get_timezone,
    }

def necessaries():
    return {
        'type' : type,
        'print' : print,
        'repr' : repr,
        'str' : str,

    }