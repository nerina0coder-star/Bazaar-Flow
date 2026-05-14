from app.models.message import Message
from app.extensions import db
from app.repositories.chamber_repository import ChamberRepository
from app.repositories.user_repository import UserRepository


class MessageRepository:
    @staticmethod
    def create(text: str, chamber_id: str, author_id: int) -> Message:
        msg = Message(content=text)
        msg.chamber = ChamberRepository.find_by_id(chamber_id)
        msg.author = UserRepository.find_by_id(author_id)
        db.session.add(msg)
        db.session.commit()
        return msg
    @staticmethod
    def edit(message_id: int, new_text: str) -> Message:
        msg = Message.query.filter_by(id=message_id).first()
        msg.text = new_text
        db.session.commit()
        return msg
    @staticmethod
    def delete_by_id(message_id: int) -> None:
        Message.query.filter_by(id=message_id).delete()
        db.session.commit()
    @staticmethod
    def find_by_id(message_id: int) -> Message:
        return Message.query.filter_by(id=message_id).first()