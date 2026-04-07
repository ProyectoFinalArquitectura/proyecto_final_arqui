"""
Fixtures compartidas para todos los tests.
Usa SQLite en memoria para no depender de PostgreSQL durante las pruebas.
"""
import pytest
from datetime import datetime, timedelta

from flask_jwt_extended import create_access_token

from app import create_app
from app.extensions import db as _db, bcrypt as _bcrypt
from app.models.user import User, RoleEnum
from app.models.event import Event, EventStatusEnum


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret-key"
    JWT_SECRET_KEY = "test-jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = 86400


@pytest.fixture()
def app():
    """Crea una instancia de la app con base de datos SQLite en memoria."""
    application = create_app(TestConfig)
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    """Cliente HTTP de prueba."""
    return app.test_client()


@pytest.fixture()
def admin_user(app):
    """Usuario con rol ADMIN."""
    user = User(
        name="Admin Test",
        email="admin@test.com",
        password=_bcrypt.generate_password_hash("password123").decode("utf-8"),
        role=RoleEnum.ADMIN,
    )
    _db.session.add(user)
    _db.session.commit()
    _db.session.refresh(user)
    return user


@pytest.fixture()
def organizer_user(app):
    """Usuario con rol ORGANIZADOR."""
    user = User(
        name="Organizer Test",
        email="organizer@test.com",
        password=_bcrypt.generate_password_hash("password123").decode("utf-8"),
        role=RoleEnum.ORGANIZADOR,
    )
    _db.session.add(user)
    _db.session.commit()
    _db.session.refresh(user)
    return user


@pytest.fixture()
def admin_token(app, admin_user):
    """JWT válido para el usuario ADMIN."""
    return create_access_token(
        identity=str(admin_user.id),
        additional_claims={"role": admin_user.role.value},
    )


@pytest.fixture()
def organizer_token(app, organizer_user):
    """JWT válido para el usuario ORGANIZADOR."""
    return create_access_token(
        identity=str(organizer_user.id),
        additional_claims={"role": organizer_user.role.value},
    )


@pytest.fixture()
def sample_event(app, organizer_user):
    """Evento activo de prueba creado por organizer_user."""
    event = Event(
        title="Evento de Prueba",
        description="Descripción del evento de prueba",
        date=datetime.utcnow() + timedelta(days=30),
        location="San Salvador",
        max_capacity=50,
        organizer_id=organizer_user.id,
        status=EventStatusEnum.ACTIVO,
    )
    _db.session.add(event)
    _db.session.commit()
    _db.session.refresh(event)
    return event
