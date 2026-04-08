from flask import Flask
from app.extensions import db, migrate, jwt, cors, bcrypt
from app.config import Config
from app.middlewares.error_handler import register_error_handlers


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {
        "origins": "*",
        "methods": ["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Authorization", "Content-Type"],
    }})
    bcrypt.init_app(app)

    register_error_handlers(app)

    from app.controllers.auth_controller import auth_bp
    from app.controllers.event_controller import event_bp
    from app.controllers.attendee_controller import attendee_bp
    from app.controllers.admin_controller import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(event_bp, url_prefix="/api/events")
    app.register_blueprint(attendee_bp, url_prefix="/api/attendees")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app