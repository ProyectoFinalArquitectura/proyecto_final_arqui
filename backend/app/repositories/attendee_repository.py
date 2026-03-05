from app.repositories.base_repository import BaseRepository
from app.models.attendee import Attendee

class AttendeeRepository(BaseRepository):
    def __init__(self):
        super().__init__(Attendee)

    def get_by_email(self, email):
        return Attendee.query.filter_by(email=email).first()