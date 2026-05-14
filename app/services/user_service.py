from app.repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash


class UserService:
    @staticmethod
    def register_user(email, password, username):
        # Business logic: check if user exists
        existing = UserRepository.find_by_email(email)
        if existing:
            raise ValueError("Email already registered")


        # Validate password strength
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

        # Create user
        return UserRepository.create(email, password, username)

    @staticmethod
    def authenticate(username, email, password):
        user_mail = UserRepository.find_by_email(email)

        if user_mail and user_mail.check_password(password) and user_mail.is_active and username == user_mail.username:
            return user_mail
        return None

    @staticmethod
    def update_profile(user_id, username, email, password):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        UserRepository.update(user, username=username, email=email, password=password)
        return user