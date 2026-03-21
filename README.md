
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

Antes de ejecutar el proyecto necesitas tener instalado:

- Python **3.12 recomendado**
- PostgreSQL
- pip
- Node.js **20+ recomendado**
- npm
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

## 7️⃣ Ejecutar seeders iniciales

Ejecutar:

```powershell
python seed_admin.py
python seed_events.py
```

`seed_admin.py` crea el usuario administrador y `seed_events.py` carga eventos/organizadores de prueba.

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

# 💻 Levantar Frontend (Next.js)

El frontend vive en `frontend/` y consume la API del backend.

## 1️⃣ Verifica que el backend esté corriendo

Antes de iniciar frontend, asegúrate de tener backend arriba en:

```
http://127.0.0.1:5000
```

## 2️⃣ Ir a la carpeta del frontend

Desde la raíz del repositorio:

```powershell
cd frontend
```

## 3️⃣ Configurar variable de entorno del frontend

Crea el archivo `frontend/.env.local` con:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5000/api
```

Si tu backend corre en otro puerto (por ejemplo 5001), ajusta la URL:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5001/api
```

## 4️⃣ Instalar dependencias

```powershell
npm install
```

## 5️⃣ Ejecutar frontend en desarrollo

```powershell
npm run dev
```

Frontend disponible en:

```
http://localhost:3000
```

## 6️⃣ Credenciales de prueba

Si ejecutaste los seeders del backend (`seed_admin.py` y `seed_events.py`):

- Admin:
  - email: `admin@admin.com`
  - password: `Admin123456`

## 7️⃣ Checklist rápido de verificación FE

- Carga `/login` correctamente.
- Login de admin funciona.
- Redirige a `/admin` después del login.
- Se pueden listar eventos sin error de conexión.

## 8️⃣ Troubleshooting FE

1. Error de conexión con API:
    - Verifica backend activo y valor de `NEXT_PUBLIC_API_BASE_URL`.
2. Cambiaste `.env.local` y no toma cambios:
    - Reinicia `npm run dev`.
3. Puerto 3000 ocupado:
    - Libera el puerto o ejecuta `npm run dev -- -p 3001`.

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

Ejecuta los tests del backend desde la carpeta `backend/`:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

Documentación detallada de testing:
- `backend/tests/README.md`

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
