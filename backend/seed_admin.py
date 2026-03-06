from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User, RoleEnum

app = create_app()

with app.app_context():
    # Borra el admin existente si hay
    existing = User.query.filter_by(email="admin@test.com").first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        print(" Admin anterior eliminado")

    # Crea admin nuevo
    admin = User(
        name="Admin",
        email="admin@test.com",
        password=bcrypt.generate_password_hash("123456").decode("utf-8"),
        role=RoleEnum.ADMIN
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin creado correctamente")
    print("   Email: admin@test.com")
    print("   Password: 123456")