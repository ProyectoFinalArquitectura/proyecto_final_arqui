from app.repositories.base_repository import BaseRepository
from app.models.registration import Registration, RegistrationStatusEnum

class RegistrationRepository(BaseRepository):
    def __init__(self):
        super().__init__(Registration)

    def get_by_event(self, event_id):
        return Registration.query.filter_by(event_id=event_id).all()

    def get_active_by_event(self, event_id):
        return Registration.query.filter_by(
            event_id=event_id,
            status=RegistrationStatusEnum.ACTIVO
        ).all()

    def get_by_attendee(self, attendee_id):
        return Registration.query.filter_by(attendee_id=attendee_id).all()

    def find_existing(self, event_id, attendee_id):
        return Registration.query.filter_by(
            event_id=event_id,
            attendee_id=attendee_id,
            status=RegistrationStatusEnum.ACTIVO
        ).first()