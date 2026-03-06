from flask import Blueprint, jsonify, request

from app.middlewares.auth_middleware import admin_required, get_current_user, token_required
from app.schemas.event_schema import EventSchema, EventUpdateSchema
from app.services.event_service import EventService

event_bp = Blueprint("events", __name__)

event_service = EventService()
event_schema = EventSchema()
events_schema = EventSchema(many=True)
event_update_schema = EventUpdateSchema()


@event_bp.get("")
@token_required
def get_events():
	user = get_current_user()
	events = event_service.get_all(user)
	return jsonify({"data": events_schema.dump(events)}), 200


@event_bp.get("/active")
@token_required
def get_active_events():
	events = event_service.get_active()
	return jsonify({"data": events_schema.dump(events)}), 200


@event_bp.get("/status/<string:status>")
@token_required
def get_events_by_status(status):
	events = event_service.get_by_status(status)
	return jsonify({"data": events_schema.dump(events)}), 200


@event_bp.get("/<int:event_id>")
@token_required
def get_event_by_id(event_id):
	user = get_current_user()
	event = event_service.get_by_id(event_id, user)
	return jsonify({"data": event_schema.dump(event)}), 200


@event_bp.post("")
@token_required
def create_event():
	user = get_current_user()
	data = event_schema.load(request.get_json() or {})
	event = event_service.create(data, user)
	return jsonify({"message": "Evento creado", "data": event_schema.dump(event)}), 201


@event_bp.put("/<int:event_id>")
@token_required
def update_event(event_id):
	user = get_current_user()
	data = event_update_schema.load(request.get_json() or {})
	event = event_service.update(event_id, data, user)
	return jsonify({"message": "Evento actualizado", "data": event_schema.dump(event)}), 200


@event_bp.patch("/<int:event_id>/cancel")
@token_required
def cancel_event(event_id):
	user = get_current_user()
	event = event_service.cancel(event_id, user)
	return jsonify({"message": "Evento cancelado", "data": event_schema.dump(event)}), 200


@event_bp.patch("/<int:event_id>/status")
@admin_required
def change_event_status(event_id):
	user = get_current_user()
	data = request.get_json() or {}

	if "status" not in data:
		return jsonify({"message": "El campo status es obligatorio"}), 400

	event = event_service.change_status(event_id, data["status"], user)
	return jsonify({"message": "Estado actualizado", "data": event_schema.dump(event)}), 200


@event_bp.delete("/<int:event_id>")
@token_required
def delete_event(event_id):
	user = get_current_user()
	event_service.delete(event_id, user)
	return jsonify({"message": "Evento eliminado"}), 200

