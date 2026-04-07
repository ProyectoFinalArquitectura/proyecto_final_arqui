"""
Pruebas para el módulo de usuarios y autenticación.
- Unitarias: validación de esquemas
- Integración: endpoints /api/auth/register, /api/auth/login, /api/auth/me
"""
from marshmallow import ValidationError
import pytest

from app.schemas.user_schema import UserSchema


# ---------------------------------------------------------------------------
# Pruebas unitarias – validación de esquema
# ---------------------------------------------------------------------------

class TestUserSchemaUnit:
    """Valida el UserSchema sin tocar la base de datos."""

    def test_schema_acepta_datos_validos(self, app):
        schema = UserSchema()
        data = schema.load(
            {"name": "Juan Perez", "email": "juan@example.com", "password": "secret123"}
        )
        assert data["name"] == "Juan Perez"
        assert data["email"] == "juan@example.com"

    def test_schema_rechaza_password_corta(self, app):
        schema = UserSchema()
        with pytest.raises(ValidationError) as exc:
            schema.load(
                {"name": "Juan", "email": "juan@example.com", "password": "abc"}
            )
        assert "password" in exc.value.messages

    def test_schema_rechaza_email_invalido(self, app):
        schema = UserSchema()
        with pytest.raises(ValidationError) as exc:
            schema.load(
                {"name": "Juan", "email": "no-es-email", "password": "secret123"}
            )
        assert "email" in exc.value.messages

    def test_schema_rechaza_nombre_corto(self, app):
        schema = UserSchema()
        with pytest.raises(ValidationError) as exc:
            schema.load(
                {"name": "J", "email": "juan@example.com", "password": "secret123"}
            )
        assert "name" in exc.value.messages

    def test_schema_requiere_nombre(self, app):
        schema = UserSchema()
        with pytest.raises(ValidationError) as exc:
            schema.load({"email": "juan@example.com", "password": "secret123"})
        assert "name" in exc.value.messages


# ---------------------------------------------------------------------------
# Pruebas de integración – endpoints HTTP
# ---------------------------------------------------------------------------

class TestRegisterEndpoint:
    """POST /api/auth/register"""

    def test_registro_exitoso(self, client):
        res = client.post(
            "/api/auth/register",
            json={"name": "Nuevo Usuario", "email": "nuevo@test.com", "password": "pass1234"},
        )
        assert res.status_code == 201
        data = res.get_json()
        assert data["message"] == "Usuario registrado"
        assert data["data"]["email"] == "nuevo@test.com"

    def test_registro_falla_email_duplicado(self, client, organizer_user):
        res = client.post(
            "/api/auth/register",
            json={
                "name": "Otro",
                "email": organizer_user.email,
                "password": "pass1234",
            },
        )
        assert res.status_code == 400
        assert "email" in res.get_json()["message"].lower() or "registrado" in res.get_json()["message"].lower()

    def test_registro_falla_sin_datos(self, client):
        res = client.post("/api/auth/register", json={})
        assert res.status_code == 400

    def test_registro_falla_password_corta(self, client):
        res = client.post(
            "/api/auth/register",
            json={"name": "Test", "email": "test2@test.com", "password": "123"},
        )
        assert res.status_code == 400


class TestLoginEndpoint:
    """POST /api/auth/login"""

    def test_login_exitoso(self, client, organizer_user):
        res = client.post(
            "/api/auth/login",
            json={"email": organizer_user.email, "password": "password123"},
        )
        assert res.status_code == 200
        data = res.get_json()
        assert "token" in data["data"]
        assert data["data"]["user"]["email"] == organizer_user.email

    def test_login_falla_password_incorrecta(self, client, organizer_user):
        res = client.post(
            "/api/auth/login",
            json={"email": organizer_user.email, "password": "wrongpassword"},
        )
        assert res.status_code == 400

    def test_login_falla_usuario_no_existe(self, client):
        res = client.post(
            "/api/auth/login",
            json={"email": "noexiste@test.com", "password": "password123"},
        )
        assert res.status_code == 400

    def test_login_falla_sin_email(self, client):
        res = client.post("/api/auth/login", json={"password": "password123"})
        assert res.status_code == 400

    def test_login_falla_sin_password(self, client):
        res = client.post("/api/auth/login", json={"email": "alguien@test.com"})
        assert res.status_code == 400


class TestMeEndpoint:
    """GET /api/auth/me"""

    def test_me_retorna_usuario_autenticado(self, client, organizer_user, organizer_token):
        res = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {organizer_token}"},
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["data"]["email"] == organizer_user.email

    def test_me_retorna_admin(self, client, admin_user, admin_token):
        res = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 200
        assert res.get_json()["data"]["role"] == "ADMIN"

    def test_me_falla_sin_token(self, client):
        res = client.get("/api/auth/me")
        assert res.status_code == 401

    def test_me_falla_token_invalido(self, client):
        res = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer token.invalido.aqui"},
        )
        # Flask-JWT-Extended devuelve 401 o 422 para tokens malformados
        assert res.status_code in (401, 422)
