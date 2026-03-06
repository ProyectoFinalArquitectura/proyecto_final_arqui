from flask import jsonify
from flask_jwt_extended.exceptions import JWTExtendedException
from marshmallow import ValidationError


def register_error_handlers(app):
	@app.errorhandler(ValidationError)
	def handle_validation_error(error):
		return jsonify({"message": "Datos inválidos", "errors": error.messages}), 400

	@app.errorhandler(ValueError)
	def handle_value_error(error):
		return jsonify({"message": str(error)}), 400

	@app.errorhandler(PermissionError)
	def handle_permission_error(error):
		return jsonify({"message": str(error)}), 403

	@app.errorhandler(JWTExtendedException)
	def handle_jwt_error(error):
		return jsonify({"message": str(error)}), 401

	@app.errorhandler(404)
	def handle_not_found(_error):
		return jsonify({"message": "Ruta no encontrada"}), 404

	@app.errorhandler(500)
	def handle_server_error(_error):
		return jsonify({"message": "Error interno del servidor"}), 500

