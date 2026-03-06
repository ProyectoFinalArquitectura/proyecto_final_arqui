from app.extensions import db
from datetime import datetime
import enum

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    ORGANIZADOR = "ORGANIZADOR"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.ORGANIZADOR.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    events = db.relationship("Event", backref="organizer", lazy=True)

    def __repr__(self):
        return f"<User {self.email} - {self.role}>"