"""
Pruebas para el módulo de eventos.
- Unitarias: validación de esquema, lógica del modelo
- Integración: endpoints /api/events
"""
from datetime import datetime, timedelta

import pytest
from marshmallow import ValidationError

from app.schemas.event_schema import EventSchema
from app.models.event import Event, EventStatusEnum


# ---------------------------------------------------------------------------
# Pruebas unitarias – validación de esquema y modelo
# ---------------------------------------------------------------------------

class TestEventSchemaUnit:
    """Valida el EventSchema sin tocar la base de datos."""

    def _valid_payload(self):
        return {
            "title": "Conferencia Tech",
            "description": "Gran conferencia",
            "date": (datetime.utcnow() + timedelta(days=10)).isoformat(),
            "location": "San Salvador",
            "max_capacity": 100,
        }

    def test_schema_acepta_datos_validos(self, app):
        schema = EventSchema()
        data = schema.load(self._valid_payload())
        assert data["title"] == "Conferencia Tech"
        assert data["max_capacity"] == 100

    def test_schema_rechaza_titulo_corto(self, app):
        schema = EventSchema()
        payload = self._valid_payload()
        payload["title"] = "AB"
        with pytest.raises(ValidationError) as exc:
            schema.load(payload)
        assert "title" in exc.value.messages

    def test_schema_rechaza_capacidad_cero(self, app):
        schema = EventSchema()
        payload = self._valid_payload()
        payload["max_capacity"] = 0
        with pytest.raises(ValidationError) as exc:
            schema.load(payload)
        assert "max_capacity" in exc.value.messages

    def test_schema_rechaza_sin_location(self, app):
        schema = EventSchema()
        payload = self._valid_payload()
        del payload["location"]
        with pytest.raises(ValidationError) as exc:
            schema.load(payload)
        assert "location" in exc.value.messages

    def test_schema_rechaza_sin_fecha(self, app):
        schema = EventSchema()
        payload = self._valid_payload()
        del payload["date"]
        with pytest.raises(ValidationError) as exc:
            schema.load(payload)
        assert "date" in exc.value.messages


class TestEventModelUnit:
    """Pruebas de lógica de negocio del modelo Event."""

    def test_evento_activo_inicial(self, app, sample_event):
        assert sample_event.is_active() is True

    def test_evento_no_activo_si_cancelado(self, app, sample_event):
        sample_event.status = EventStatusEnum.CANCELADO
        assert sample_event.is_active() is False

    def test_check_sold_out_sin_registros(self, app, sample_event):
        # Sin registros no debe cambiar a SOLD_OUT
        sample_event.check_sold_out()
        assert sample_event.status == EventStatusEnum.ACTIVO


# ---------------------------------------------------------------------------
# Pruebas de integración – endpoints HTTP
# ---------------------------------------------------------------------------

class TestGetEvents:
    """GET /api/events"""

    def test_organizador_ve_sus_eventos(self, client, organizer_token, sample_event):
        res = client.get(
            "/api/events",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 200
        events = res.get_json()["data"]
        assert len(events) >= 1
        assert any(e["id"] == sample_event.id for e in events)

    def test_admin_ve_todos_los_eventos(self, client, admin_token, sample_event):
        res = client.get(
            "/api/events",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 200
        assert isinstance(res.get_json()["data"], list)

    def test_sin_token_retorna_401(self, client):
        res = client.get("/api/events")
        assert res.status_code == 401


class TestCreateEvent:
    """POST /api/events"""

    def _payload(self):
        return {
            "title": "Nuevo Evento",
            "description": "Descripción",
            "date": (datetime.utcnow() + timedelta(days=20)).isoformat(),
            "location": "Santa Ana",
            "max_capacity": 200,
        }

    def test_crea_evento_exitosamente(self, client, organizer_token):
        res = client.post(
            "/api/events",
            json=self._payload(),
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 201
        data = res.get_json()
        assert data["data"]["title"] == "Nuevo Evento"
        assert data["data"]["status"] == "ACTIVO"

    def test_evento_creado_tiene_organizer_id(self, client, organizer_user, organizer_token):
        res = client.post(
            "/api/events",
            json=self._payload(),
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 201
        assert res.get_json()["data"]["organizer_id"] == organizer_user.id

    def test_falla_sin_titulo(self, client, organizer_token):
        payload = self._payload()
        del payload["title"]
        res = client.post(
            "/api/events",
            json=payload,
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 400

    def test_falla_sin_token(self, client):
        res = client.post("/api/events", json=self._payload())
        assert res.status_code == 401


class TestUpdateEvent:
    """PUT /api/events/<id>"""

    def test_organizador_actualiza_su_evento(self, client, organizer_token, sample_event):
        res = client.put(
            f"/api/events/{sample_event.id}",
            json={"title": "Título Actualizado", "location": "Nueva Sede"},
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 200
        assert res.get_json()["data"]["title"] == "Título Actualizado"

    def test_organizador_no_puede_editar_evento_ajeno(
        self, client, admin_user, admin_token, organizer_token, app
    ):
        from app.extensions import db
        from app.models.event import Event, EventStatusEnum

        otro_evento = Event(
            title="Evento del Admin",
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

        res = client.put(
            f"/api/events/{otro_evento.id}",
            json={"title": "Modificado"},
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 403


class TestCancelEvent:
    """PATCH /api/events/<id>/cancel"""

    def test_organizador_cancela_su_evento(self, client, organizer_token, sample_event):
        res = client.patch(
            f"/api/events/{sample_event.id}/cancel",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 200
        assert res.get_json()["data"]["status"] == "CANCELADO"

    def test_no_se_puede_cancelar_dos_veces(self, client, organizer_token, sample_event):
        client.patch(
            f"/api/events/{sample_event.id}/cancel",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        res = client.patch(
            f"/api/events/{sample_event.id}/cancel",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 400


class TestDeleteEvent:
    """DELETE /api/events/<id>"""

    def test_organizador_elimina_su_evento(self, client, organizer_token, sample_event):
        res = client.delete(
            f"/api/events/{sample_event.id}",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 200

    def test_evento_no_existe_tras_eliminacion(self, client, organizer_token, sample_event):
        client.delete(
            f"/api/events/{sample_event.id}",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        res = client.get(
            f"/api/events/{sample_event.id}",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 400


class TestChangeEventStatus:
    """PATCH /api/events/<id>/status (solo admin)"""

    def test_admin_cambia_estado(self, client, admin_token, sample_event):
        res = client.patch(
            f"/api/events/{sample_event.id}/status",
            json={"status": "FINALIZADO"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 200
        assert res.get_json()["data"]["status"] == "FINALIZADO"

    def test_organizador_no_puede_cambiar_estado(self, client, organizer_token, sample_event):
        res = client.patch(
            f"/api/events/{sample_event.id}/status",
            json={"status": "FINALIZADO"},
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 403
