"""
Pruebas de humo (Smoke Tests).
Verifican que la aplicación arranca correctamente y que los endpoints
principales son accesibles (responden, no devuelven 404 ni 500).
"""


class TestSmokeAppStartup:
    """Verifica que la app levanta y la BD se inicializa sin errores."""

    def test_app_is_created(self, app):
        assert app is not None

    def test_app_is_in_testing_mode(self, app):
        assert app.config["TESTING"] is True

    def test_database_tables_created(self, app):
        from app.extensions import db
        # Si las tablas no existieran, este inspect fallaría
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        assert "users" in tables
        assert "events" in tables
        assert "attendees" in tables
        assert "registrations" in tables


class TestSmokeAuthEndpoints:
    """Verifica que los endpoints de autenticación responden."""

    def test_register_endpoint_exists(self, client):
        """POST /api/auth/register debe responder (no 404)."""
        res = client.post("/api/auth/register", json={})
        assert res.status_code != 404

    def test_login_endpoint_exists(self, client):
        """POST /api/auth/login debe responder (no 404)."""
        res = client.post("/api/auth/login", json={})
        assert res.status_code != 404

    def test_me_endpoint_exists(self, client):
        """GET /api/auth/me sin token debe devolver 401, no 404."""
        res = client.get("/api/auth/me")
        assert res.status_code == 401

    def test_unknown_route_returns_404(self, client):
        """Rutas inexistentes deben devolver 404."""
        res = client.get("/api/ruta-que-no-existe")
        assert res.status_code == 404


class TestSmokeEventEndpoints:
    """Verifica que los endpoints de eventos responden."""

    def test_events_endpoint_requires_auth(self, client):
        """GET /api/events sin token debe devolver 401."""
        res = client.get("/api/events")
        assert res.status_code == 401

    def test_create_event_requires_auth(self, client):
        """POST /api/events sin token debe devolver 401."""
        res = client.post("/api/events", json={})
        assert res.status_code == 401

    def test_active_events_endpoint_requires_auth(self, client):
        """GET /api/events/active sin token debe devolver 401."""
        res = client.get("/api/events/active")
        assert res.status_code == 401


class TestSmokeAttendeeEndpoints:
    """Verifica que los endpoints de asistentes responden."""

    def test_attendees_endpoint_requires_auth(self, client):
        """GET /api/attendees sin token debe devolver 401."""
        res = client.get("/api/attendees")
        assert res.status_code == 401

    def test_register_attendee_requires_auth(self, client):
        """POST /api/attendees/event/1/register sin token debe devolver 401."""
        res = client.post("/api/attendees/event/1/register", json={})
        assert res.status_code == 401
