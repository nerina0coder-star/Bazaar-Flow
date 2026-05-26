import datetime

from app.models import Chamber
from app.repositories.chamber_repository import ChamberRepository


def role_to_persian(value):
    role = {
        'member' : 'عضو',
        'owner' : 'صاحب'
    }
    return role[value]

def members_online(value: Chamber):
    chamber = ChamberRepository.find_by_id(value.id)

    actives = 0
    for member in chamber.users:
        if member.is_online():
            actives += 1

    return actives