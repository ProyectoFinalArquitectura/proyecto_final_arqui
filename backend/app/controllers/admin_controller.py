from flask import Blueprint, jsonify

from app.middlewares.auth_middleware import admin_required
from app.repositories.event_repository import EventRepository
from app.repositories.registration_repository import RegistrationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.event_schema import EventSchema
from app.schemas.registration_schema import RegistrationSchema
from app.schemas.user_schema import UserSchema
from app.models.user import RoleEnum
from app.models.event import EventStatusEnum

admin_bp = Blueprint("admin", __name__)

event_repo = EventRepository()
registration_repo = RegistrationRepository()
user_repo = UserRepository()

events_schema = EventSchema(many=True)
users_schema = UserSchema(many=True)
registrations_schema = RegistrationSchema(many=True)


@admin_bp.get("/stats")
@admin_required
def stats():
	events = event_repo.get_all()
	users = user_repo.get_all()
	registrations = registration_repo.get_all()

	return jsonify(
		{
			"data": {
				"events": len(events),
				"users": len(users),
				"registrations": len(registrations),
			}
		}
	), 200


@admin_bp.get("/events")
@admin_required
def get_all_events():
	return jsonify({"data": events_schema.dump(event_repo.get_all())}), 200


@admin_bp.get("/users")
@admin_required
def get_all_users():
	return jsonify({"data": users_schema.dump(user_repo.get_all())}), 200


@admin_bp.get("/users/role/<string:role>")
@admin_required
def get_users_by_role(role):
	role_value = RoleEnum(role)
	return jsonify({"data": users_schema.dump(user_repo.get_by_role(role_value))}), 200


@admin_bp.get("/registrations")
@admin_required
def get_all_registrations():
	return jsonify({"data": registrations_schema.dump(registration_repo.get_all())}), 200


@admin_bp.get("/events/status/<string:status>")
@admin_required
def get_events_by_status(status):
	status_value = EventStatusEnum(status)
	return jsonify({"data": events_schema.dump(event_repo.get_by_status(status_value))}), 200


@admin_bp.get("/events/active")
@admin_required
def get_active_events():
	return jsonify({"data": events_schema.dump(event_repo.get_active_events())}), 200


@admin_bp.get("/registrations/event/<int:event_id>")
@admin_required
def get_registrations_by_event(event_id):
	return jsonify({"data": registrations_schema.dump(registration_repo.get_by_event(event_id))}), 200


@admin_bp.get("/registrations/attendee/<int:attendee_id>")
@admin_required
def get_registrations_by_attendee(attendee_id):
	return jsonify({"data": registrations_schema.dump(registration_repo.get_by_attendee(attendee_id))}), 200

@admin_bp.route("/setup", methods=["POST"])
def create_first_admin():
    from app.extensions import bcrypt
    from app.models.user import User
    from flask import request

    existing_admin = user_repo.get_by_role(RoleEnum.ADMIN)
    if existing_admin:
        return jsonify({"error": "Ya existe un administrador"}), 403

    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    admin = User(name=data["name"], email=data["email"], password=hashed_pw, role=RoleEnum.ADMIN)
    user_repo.save(admin)
    return jsonify({"message": "Administrador creado"}), 201