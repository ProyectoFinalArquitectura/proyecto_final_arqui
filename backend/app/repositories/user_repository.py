from app.repositories.base_repository import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def get_by_role(self, role):
        return User.query.filter_by(role=role).all()