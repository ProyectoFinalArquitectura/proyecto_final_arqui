from flask import Blueprint, jsonify, request

from app.middlewares.auth_middleware import get_current_user, token_required
from app.schemas.attendee_schema import AttendeeSchema
from app.schemas.registration_schema import RegistrationSchema
from app.services.attendee_service import AttendeeService

attendee_bp = Blueprint("attendees", __name__)

attendee_service = AttendeeService()
attendee_schema = AttendeeSchema()
attendees_schema = AttendeeSchema(many=True)
registration_schema = RegistrationSchema()
registrations_schema = RegistrationSchema(many=True)


@attendee_bp.get("")
@token_required
def get_all_attendees():
	user = get_current_user()
	attendees = attendee_service.get_all_attendees(user)
	return jsonify({"data": attendees_schema.dump(attendees)}), 200


@attendee_bp.get("/<int:attendee_id>")
@token_required
def get_attendee_by_id(attendee_id):
	user = get_current_user()
	attendee = attendee_service.get_attendee_by_id(attendee_id, user)
	return jsonify({"data": attendee_schema.dump(attendee)}), 200


@attendee_bp.get("/<int:attendee_id>/registrations")
@token_required
def get_attendee_registrations(attendee_id):
	user = get_current_user()
	registrations = attendee_service.get_attendee_registrations(attendee_id, user)
	return jsonify({"data": registrations_schema.dump(registrations)}), 200


@attendee_bp.post("/event/<int:event_id>/register")
@token_required
def register_attendee(event_id):
	user = get_current_user()
	data = attendee_schema.load(request.get_json() or {})
	registration = attendee_service.register_to_event(event_id, data, user)
	return jsonify({"message": "Inscripción creada", "data": registration_schema.dump(registration)}), 201


@attendee_bp.get("/event/<int:event_id>")
@token_required
def get_event_attendees(event_id):
	user = get_current_user()
	registrations = attendee_service.get_event_attendees(event_id, user)
	return jsonify({"data": registrations_schema.dump(registrations)}), 200


@attendee_bp.patch("/registration/<int:registration_id>/cancel")
@token_required
def cancel_registration(registration_id):
	user = get_current_user()
	registration = attendee_service.cancel_registration(registration_id, user)
	return jsonify(
		{
			"message": "Inscripción cancelada",
			"data": registration_schema.dump(registration),
		}
	), 200

