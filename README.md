
# 🚀 Sistema de Gestión de Eventos — Backend

Backend para un sistema de gestión de eventos desarrollado con **Flask**, **PostgreSQL** y **JWT Authentication**.

Permite gestionar:
- Usuarios
- Eventos
- Asistentes
- Registros
- Panel de administración

---

# 📋 Requisitos previos

Antes de ejecutar el proyecto necesitas tener instalado:

- Python **3.12 recomendado**
- PostgreSQL
- pip
- Git (opcional)

⚠️ Python 3.14 puede generar errores con `psycopg2` en Windows.

---

# ⚙️ Configuración del entorno

## 1️⃣ Clonar el repositorio

```bash
git clone <repo-url>
cd proyecto_final_arqui/backend
```

---

## 2️⃣ Crear la base de datos en PostgreSQL

```sql
CREATE DATABASE eventos_db;
```

---

## 3️⃣ Crear archivo `.env`

Dentro de la carpeta `backend/` crea un archivo `.env`:

```env
SECRET_KEY=supersecreto123
JWT_SECRET_KEY=jwtsecreto456
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/eventos_db
```

Reemplaza `TU_PASSWORD` por tu contraseña de PostgreSQL.

⚠️ `.env` no debe subirse a GitHub.

---

## 4️⃣ Crear entorno virtual

```powershell
py -3.12 -m venv .venv
```

Activar entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego activar otra vez:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 5️⃣ Instalar dependencias

```powershell
pip install -r requirements.txt
```

Si aparece error con PostgreSQL:

```powershell
pip install psycopg2-binary
```

---

## 6️⃣ Ejecutar migraciones

```powershell
$env:FLASK_APP="run.py"
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

Esto crea todas las tablas en la base de datos.

---

## 7️⃣ Crear usuario administrador (Seeder)

Crea el archivo:

`backend/seed_admin.py`

```python
from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User, RoleEnum

app = create_app()

with app.app_context():
    existing_admin = User.query.filter_by(email="admin@admin.com").first()

    if existing_admin:
        print("Admin ya existe")
    else:
        hashed_password = bcrypt.generate_password_hash("Admin123456").decode("utf-8")

        admin = User(
            name="Administrador",
            email="admin@admin.com",
            password=hashed_password,
            role=RoleEnum.ADMIN
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin creado correctamente")
```

Ejecutar:

```powershell
python seed_admin.py
```

Credenciales:

```
email: admin@admin.com
password: Admin123456
```

---

## 8️⃣ Correr el servidor

```powershell
python run.py
```

Servidor disponible en:

```
http://localhost:5000
```

---

# 📡 Endpoints

## Auth — `/api/auth`

| Método | Ruta | Descripción |
|------|------|------|
| POST | /register | Registrar organizador |
| POST | /login | Login y obtener JWT |

---

## Eventos — `/api/events`

| Método | Ruta | Descripción |
|------|------|------|
| GET | / | Listar eventos |
| GET | /:id | Ver evento |
| POST | / | Crear evento |
| PUT | /:id | Editar evento |
| PATCH | /:id/cancel | Cancelar evento |
| PATCH | /:id/status | Cambiar estado (Admin) |

---

## Asistentes — `/api/attendees`

| Método | Ruta | Descripción |
|------|------|------|
| GET | /events/:id | Ver asistentes |
| POST | /events/:id/register | Registrar asistente |
| PATCH | /registrations/:id/cancel | Cancelar inscripción |

---

## Admin — `/api/admin`

(Requiere JWT + rol ADMIN)

| Método | Ruta | Descripción |
|------|------|------|
| GET | /users | Listar usuarios |
| PUT | /users/:id | Editar usuario |
| DELETE | /users/:id | Eliminar usuario |
| GET | /dashboard | Estadísticas |

---

# 🧪 Tests

```powershell
pytest tests/
```

---

# 🐳 Docker

```powershell
docker-compose up --build
```

---

# 👨‍💻 Tecnologías

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- PostgreSQL
- JWT
- Pytest
- Docker
