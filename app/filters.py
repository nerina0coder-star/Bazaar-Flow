from app.models import Chamber


def role_to_persian(value):
    role = {
        'member': 'عضو',
        'owner': 'صاحب'
    }
    return role[value]


def members_online(value: Chamber):
    chamber = value

    actives = 0
    for member in chamber.users:
        if member.is_online():
            actives += 1

    return actives
