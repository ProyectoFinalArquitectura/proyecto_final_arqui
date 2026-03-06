from flask import Blueprint, jsonify, request

from app.middlewares.auth_middleware import get_current_user, token_required
from app.schemas.user_schema import UserSchema
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

auth_service = AuthService()
user_schema = UserSchema()


@auth_bp.post("/register")
def register():
	data = user_schema.load(request.get_json() or {})
	user = auth_service.register(data)
	return jsonify({"message": "Usuario registrado", "data": user_schema.dump(user)}), 201


@auth_bp.post("/login")
def login():
	data = request.get_json() or {}
	email = data.get("email")
	password = data.get("password")

	if not email or not password:
		return jsonify({"message": "Email y password son obligatorios"}), 400

	token, user = auth_service.login(data)
	return jsonify(
		{
			"message": "Login exitoso",
			"data": {
				"token": token,
				"user": user_schema.dump(user),
			},
		}
	), 200


@auth_bp.get("/me")
@token_required
def me():
	user = get_current_user()
	return jsonify({"data": user_schema.dump(user)}), 200

