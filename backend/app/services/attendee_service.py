from app.repositories.attendee_repository import AttendeeRepository
from app.repositories.registration_repository import RegistrationRepository
from app.repositories.event_repository import EventRepository
from app.models.attendee import Attendee
from app.models.registration import Registration
from app.models.event import EventStatusEnum
from app.models.user import RoleEnum

attendee_repo = AttendeeRepository()
registration_repo = RegistrationRepository()
event_repo = EventRepository()

class AttendeeService:
    def register_to_event(self, event_id, data, user):
        event = event_repo.get_by_id(event_id)
        if not event:
            raise ValueError("Evento no encontrado")
        if user.role != RoleEnum.ADMIN and event.organizer_id != user.id:
            raise PermissionError("No tienes permiso para registrar asistentes en este evento")
        if event.status != EventStatusEnum.ACTIVO:
            raise ValueError("Solo se pueden registrar asistentes en eventos ACTIVOS")
        attendee = attendee_repo.get_by_email(data["email"])
        if not attendee:
            attendee = Attendee(name=data["name"], email=data["email"], phone=data.get("phone", ""))
            attendee_repo.save(attendee)
        existing = registration_repo.find_existing(event_id, attendee.id)
        if existing:
            raise ValueError("El asistente ya esta inscrito en este evento")
        registration = Registration(event_id=event_id, attendee_id=attendee.id)
        registration_repo.save(registration)
        event.check_sold_out()
        event_repo.commit()
        return registration

    def get_event_attendees(self, event_id, user):
        event = event_repo.get_by_id(event_id)
        if not event:
            raise ValueError("Evento no encontrado")
        if user.role != RoleEnum.ADMIN and event.organizer_id != user.id:
            raise PermissionError("No tienes permiso para ver los asistentes de este evento")
        return registration_repo.get_active_by_event(event_id)

    def cancel_registration(self, registration_id, user):
        registration = registration_repo.get_by_id(registration_id)
        if not registration:
            raise ValueError("Inscripcion no encontrada")
        event = event_repo.get_by_id(registration.event_id)
        if user.role != RoleEnum.ADMIN and event.organizer_id != user.id:
            raise PermissionError("No tienes permiso para cancelar esta inscripcion")
        registration.cancel()
        registration_repo.commit()
        return registration