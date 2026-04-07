# Backend – Eventos API

API REST construida con Flask + PostgreSQL para gestión de eventos, organizadores y asistentes.

---

## Requisitos previos

- Python 3.12+
- PostgreSQL 16 (o Docker)

---

## Instalación local

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

Configura las variables de entorno en `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:root@localhost:5432/eventos_db
SECRET_KEY=supersecreto123
JWT_SECRET_KEY=jwtsecreto456
```

Aplica migraciones y corre el servidor:

```bash
flask db upgrade
python run.py
```

---

## Correr con Docker

```bash
# Desde la raíz del proyecto (donde está el docker-compose.yml principal)
docker compose up --build

# Para poblar la base de datos con datos de prueba:
docker compose run --rm seed
```

El backend queda disponible en `http://localhost:5001`.

---

## Pruebas

Las pruebas usan **SQLite en memoria** – no necesitas PostgreSQL corriendo.

### Instalar dependencias de prueba

```bash
pip install -r requirements.txt
```

### Correr todas las pruebas

```bash
cd backend
python -m pytest tests/ -v
```

### Correr por tipo

```bash
# Solo pruebas de humo
python -m pytest tests/test_smoke.py -v

# Solo pruebas de usuarios/auth
python -m pytest tests/test_users.py -v

# Solo pruebas de eventos
python -m pytest tests/test_events.py -v

# Solo pruebas de asistentes
python -m pytest tests/test_attendees.py -v
```

### Resumen de pruebas incluidas

| Archivo               | Tipo          | Cantidad | Descripción                                           |
|-----------------------|---------------|----------|-------------------------------------------------------|
| `test_smoke.py`       | Humo          | 9        | App levanta, endpoints existen y responden            |
| `test_users.py`       | Unitaria      | 5        | Validación de UserSchema                              |
| `test_users.py`       | Integración   | 9        | Register, Login, Me endpoints                        |
| `test_events.py`      | Unitaria      | 8        | Validación de EventSchema + lógica del modelo         |
| `test_events.py`      | Integración   | 14       | CRUD eventos, permisos, cambio de estado              |
| `test_attendees.py`   | Integración   | 11       | Inscripción, cancelación, listado de asistentes       |
| **Total**             |               | **66**   |                                                       |

---

## Estructura del proyecto

```
backend/
├── app/
│   ├── controllers/    # Blueprints y rutas HTTP
│   ├── models/         # Modelos SQLAlchemy
│   ├── repositories/   # Acceso a base de datos
│   ├── schemas/        # Validación con Marshmallow
│   ├── services/       # Lógica de negocio
│   ├── middlewares/    # Auth y manejo de errores
│   └── utils/          # Helpers JWT y respuestas
├── migrations/         # Migraciones Alembic
├── tests/
│   ├── conftest.py         # Fixtures compartidas
│   ├── test_smoke.py       # Pruebas de humo
│   ├── test_users.py       # Pruebas de autenticación
│   ├── test_events.py      # Pruebas de eventos
│   └── test_attendees.py   # Pruebas de asistentes
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
