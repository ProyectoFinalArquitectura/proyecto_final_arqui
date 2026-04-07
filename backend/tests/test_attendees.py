"""
Pruebas para el módulo de asistentes e inscripciones.
- Integración: endpoints /api/attendees
"""
from datetime import datetime, timedelta

from app.extensions import db
from app.models.attendee import Attendee
from app.models.event import Event, EventStatusEnum
from app.models.registration import Registration


# ---------------------------------------------------------------------------
# Pruebas de integración – inscripción a eventos
# ---------------------------------------------------------------------------

class TestRegisterAttendee:
    """POST /api/attendees/event/<id>/register"""

    def _attendee_payload(self):
        return {
            "name": "Pedro Ramirez",
            "email": "pedro@asistente.com",
            "phone": "76543210",
        }

    def test_registro_exitoso(self, client, organizer_token, sample_event):
        res = client.post(
            f"/api/attendees/event/{sample_event.id}/register",
            json=self._attendee_payload(),
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 201
        data = res.get_json()
        assert data["message"] == "Inscripción creada"
        assert data["data"]["status"] == "ACTIVO"

    def test_no_duplicar_inscripcion(self, client, organizer_token, sample_event):
        payload = self._attendee_payload()
        client.post(
            f"/api/attendees/event/{sample_event.id}/register",
            json=payload,
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        res = client.post(
            f"/api/attendees/event/{sample_event.id}/register",
            json=payload,
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 400

    def test_falla_evento_cancelado(self, client, organizer_token, sample_event):
        # Cancelamos el evento primero
        client.patch(
            f"/api/events/{sample_event.id}/cancel",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        res = client.post(
            f"/api/attendees/event/{sample_event.id}/register",
            json=self._attendee_payload(),
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 400

    def test_falla_evento_no_existe(self, client, organizer_token):
        res = client.post(
            "/api/attendees/event/99999/register",
            json=self._attendee_payload(),
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 400

    def test_falla_sin_token(self, client, sample_event):
        res = client.post(
            f"/api/attendees/event/{sample_event.id}/register",
            json=self._attendee_payload(),
        )
        assert res.status_code == 401

    def test_organizador_no_puede_registrar_en_evento_ajeno(
        self, client, organizer_token, admin_user, app
    ):
        otro_evento = Event(
            title="Evento Ajeno",
            description="",
            date=datetime.utcnow() + timedelta(days=5),
            location="Lugar",
            max_capacity=10,
            organizer_id=admin_user.id,
            status=EventStatusEnum.ACTIVO,
        )
        db.session.add(otro_evento)
        db.session.commit()
        db.session.refresh(otro_evento)

        res = client.post(
            f"/api/attendees/event/{otro_evento.id}/register",
            json=self._attendee_payload(),
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 403


class TestGetEventAttendees:
    """GET /api/attendees/event/<id>"""

    def test_organizador_ve_asistentes_de_su_evento(
        self, client, organizer_token, sample_event
    ):
        # Primero inscribimos un asistente
        client.post(
            f"/api/attendees/event/{sample_event.id}/register",
            json={"name": "Ana Lopez", "email": "ana@test.com"},
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        res = client.get(
            f"/api/attendees/event/{sample_event.id}",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 200
        registrations = res.get_json()["data"]
        assert len(registrations) >= 1

    def test_falla_sin_token(self, client, sample_event):
        res = client.get(f"/api/attendees/event/{sample_event.id}")
        assert res.status_code == 401


class TestCancelRegistration:
    """PATCH /api/attendees/registration/<id>/cancel"""

    def test_cancela_inscripcion_exitosamente(
        self, client, organizer_token, sample_event
    ):
        # Inscribir asistente
        res = client.post(
            f"/api/attendees/event/{sample_event.id}/register",
            json={"name": "Carlos Molina", "email": "carlos@test.com"},
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        registration_id = res.get_json()["data"]["id"]

        # Cancelar inscripción
        res = client.patch(
            f"/api/attendees/registration/{registration_id}/cancel",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 200
        assert res.get_json()["data"]["status"] == "CANCELADO"

    def test_falla_inscripcion_no_existe(self, client, organizer_token):
        res = client.patch(
            "/api/attendees/registration/99999/cancel",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 400

    def test_falla_sin_token(self, client):
        res = client.patch("/api/attendees/registration/1/cancel")
        assert res.status_code == 401


class TestGetAllAttendees:
    """GET /api/attendees (solo ADMIN)"""

    def test_admin_puede_ver_todos_los_asistentes(
        self, client, admin_token, organizer_user, organizer_token, sample_event
    ):
        # Inscribir un asistente primero
        client.post(
            f"/api/attendees/event/{sample_event.id}/register",
            json={"name": "Maria Gomez", "email": "maria@test.com"},
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        res = client.get(
            "/api/attendees",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 200
        assert isinstance(res.get_json()["data"], list)

    def test_organizador_no_puede_ver_todos_los_asistentes(
        self, client, organizer_token
    ):
        res = client.get(
            "/api/attendees",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 403
