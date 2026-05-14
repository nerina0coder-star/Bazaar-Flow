from app.models.chamber import Chamber
from app.repositories.chamber_repository import ChamberRepository
from app.repositories.user_repository import UserRepository


class ChamberService:

    @staticmethod
    def create_chamber(name: str, entrance_code: str) -> Chamber:
        exists = ChamberRepository.find_by_name(name)

        if exists:
            raise ValueError("Chamber already exists")
        return ChamberRepository.create_chamber(name, entrance_code)

    @staticmethod
    def rename_chamber(chamber_id: int, name: str) -> Chamber:
        not_found = not ChamberRepository.find_by_id(chamber_id)
        if not_found:
            raise ValueError("Chamber not found")

        ChamberRepository.edit_chamber(chamber_id, name)
        return ChamberRepository.find_by_id(chamber_id)

    @staticmethod
    def remove(chamber_id: int):

        not_found = not ChamberRepository.find_by_id(chamber_id)
        if not_found:
            raise ValueError("Chamber not found")

        ChamberRepository.delete_chamber(chamber_id)

    @staticmethod
    def remove_user(user_id: int, chamber_id: int):

        usr_not_found = not UserRepository.find_by_id(user_id)
        chm_not_found = not ChamberRepository.find_by_id(chamber_id)


        if usr_not_found:
            raise ValueError("User not found")
        if chm_not_found:
            raise ValueError("Chamber not found")

        ChamberRepository.remove_user_from(chamber_id, user_id)

    @staticmethod
    def add_user(chamber_id: int, user_id: int):
        if ChamberRepository.find_by_id(chamber_id) is None:
            raise ValueError("Chamber not found")
        if UserRepository.find_by_id(user_id) is None:
            raise ValueError("User not found")

        ChamberRepository.add_user(chamber_id, user_id)