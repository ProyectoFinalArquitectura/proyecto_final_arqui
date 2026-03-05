from app.repositories.base_repository import BaseRepository
from app.models.event import Event, EventStatusEnum

class EventRepository(BaseRepository):
    def __init__(self):
        super().__init__(Event)

    def get_by_organizer(self, organizer_id):
        return Event.query.filter_by(organizer_id=organizer_id).all()

    def get_by_status(self, status):
        return Event.query.filter_by(status=status).all()

    def get_active_events(self):
        return Event.query.filter_by(status=EventStatusEnum.ACTIVO).all()