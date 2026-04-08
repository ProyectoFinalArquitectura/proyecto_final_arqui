from app.repositories.event_repository import EventRepository
from app.models.event import Event, EventStatusEnum
from app.models.user import RoleEnum

event_repo = EventRepository()

class EventService:
    def get_all(self, user):
        if user.role == RoleEnum.ADMIN:
            return event_repo.get_all()
        return event_repo.get_by_organizer(user.id)

    def get_active(self):
        return event_repo.get_active_events()

    def get_by_status(self, status):
        return event_repo.get_by_status(EventStatusEnum(status))

    def get_by_id(self, event_id, user):
        event = event_repo.get_by_id(event_id)
        if not event:
            raise ValueError("Evento no encontrado")
        if user.role != RoleEnum.ADMIN and event.organizer_id != user.id:
            raise PermissionError("No tienes permiso para ver este evento")
        return event

    def create(self, data, user):
        raw_image_url = data.get("image_url")
        image_url = raw_image_url.strip() if isinstance(raw_image_url, str) else raw_image_url
        event = Event(
            title=data["title"], description=data.get("description", ""),
            image_url=image_url or None,
            date=data["date"], location=data["location"],
            max_capacity=data["max_capacity"], organizer_id=user.id
        )
        return event_repo.save(event)

    def update(self, event_id, data, user):
        event = self.get_by_id(event_id, user)
        if event.status == EventStatusEnum.CANCELADO:
            raise ValueError("No se puede editar un evento cancelado")
        for field in ["title", "description", "date", "location", "max_capacity", "image_url"]:
            if field in data:
                if field == "image_url" and isinstance(data[field], str):
                    setattr(event, field, data[field].strip() or None)
                else:
                    setattr(event, field, data[field])
        event_repo.commit()
        return event

    def cancel(self, event_id, user):
        event = self.get_by_id(event_id, user)
        if event.status == EventStatusEnum.CANCELADO:
            raise ValueError("El evento ya esta cancelado")
        event.status = EventStatusEnum.CANCELADO
        event_repo.commit()
        return event

    def change_status(self, event_id, status, user):
        if user.role != RoleEnum.ADMIN:
            raise PermissionError("Solo el administrador puede cambiar el estado")
        event = event_repo.get_by_id(event_id)
        if not event:
            raise ValueError("Evento no encontrado")
        event.status = EventStatusEnum(status)
        event_repo.commit()
        return event

    def finish(self, event_id, user):
        event = self.get_by_id(event_id, user)
        if event.status not in (EventStatusEnum.ACTIVO, EventStatusEnum.SOLD_OUT):
            raise ValueError("Solo se puede finalizar un evento activo o sold out")
        event.status = EventStatusEnum.FINALIZADO
        event_repo.commit()
        return event

    def reactivate(self, event_id, user):
        event = self.get_by_id(event_id, user)
        if event.status != EventStatusEnum.FINALIZADO:
            raise ValueError("Solo se puede reactivar un evento finalizado")
        event.status = EventStatusEnum.ACTIVO
        event_repo.commit()
        return event

    def uncancel(self, event_id, user):
        event = self.get_by_id(event_id, user)
        if event.status != EventStatusEnum.CANCELADO:
            raise ValueError("El evento no esta cancelado")
        event.status = EventStatusEnum.ACTIVO
        event_repo.commit()
        return event

    def delete(self, event_id, user):
        event = self.get_by_id(event_id, user)
        event_repo.delete(event)
        return True