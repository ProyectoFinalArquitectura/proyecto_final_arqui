
# 🚀 Sistema de Gestión de Eventos 

Sistema de gestión de eventos con:

- **Backend**: Flask, PostgreSQL y JWT Authentication.
- **Frontend**: Next.js, React y TypeScript.

Permite gestionar:
- Usuarios
- Eventos
- Asistentes
- Registros
- Panel de administración

---

# 📋 Requisitos previos

Para ejecutar el proyecto ahora solo necesitas:

- Docker Desktop (o Docker Engine + Docker Compose)
- Git (opcional)

No necesitas instalar Python, PostgreSQL ni Node.js en tu maquina para correr la app.

---

# ⚙️ Inicio rapido (solo Docker)

## 1️⃣ Clonar el repositorio

```bash
git clone <repo-url>
cd proyecto_final_arqui
```

## 2️⃣ Levantar todo el stack

Desde la raiz del proyecto:

```powershell
docker compose up --build
```

Esto levanta automaticamente:

- `db` (PostgreSQL)
- `backend` (Flask API)
- `seed` (carga datos iniciales)
- `frontend` (Next.js)

## 3️⃣ Acceder a los servicios

- Frontend: http://localhost:3000
- Backend API: http://localhost:5001
- PostgreSQL: localhost:5432

Credenciales admin de desarrollo (seed):

- email: `admin@admin.com`
- password: `Admin123456`

## 4️⃣ Detener servicios

```powershell
docker compose down
```

Para eliminar tambien volumenes de datos:

```powershell
docker compose down -v
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

Comandos utiles desde la raiz del proyecto:

```powershell
# construir y levantar todo
docker compose up --build

# detener servicios
docker compose down

# detener y eliminar volumenes
docker compose down -v
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
