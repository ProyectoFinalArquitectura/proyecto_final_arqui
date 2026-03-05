# 🚀 Sistema de Gestión de Eventos — Backend

## Requisitos previos

- Python 3.11+
- PostgreSQL instalado y corriendo
- pip

---

## ⚙️ Configuración del entorno

### 1. Crear la base de datos en PostgreSQL

Abre pgAdmin o psql y ejecuta:

```sql
CREATE DATABASE eventos_db;
```

---

### 2. Crear el archivo `.env`

Crea un archivo `.env` dentro de la carpeta `backend/` con el siguiente contenido:

```env
SECRET_KEY=supersecreto123
JWT_SECRET_KEY=jwtsecreto456
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/eventos_db
```

> ⚠️ Reemplaza `TU_PASSWORD` con tu contraseña de PostgreSQL.  
> ⚠️ El archivo `.env` **nunca se sube a GitHub** — ya está en el `.gitignore`.

---

### 3. Instalar dependencias

Desde la carpeta `backend/` corre:

```powershell
pip install -r requirements.txt
```

---

### 4. Inicializar las migraciones

```powershell
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

> Esto crea automáticamente todas las tablas en la base de datos.

---

### 5. Correr el servidor

```powershell
python run.py
```

El servidor estará disponible en: `http://localhost:5000`

---

## 📡 Endpoints disponibles

### Auth — `/api/auth`
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/register` | Registrar nuevo organizador |
| POST | `/login` | Login, devuelve JWT |

### Eventos — `/api/events` *(requiere JWT)*
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Listar eventos |
| GET | `/:id` | Ver evento |
| POST | `/` | Crear evento |
| PUT | `/:id` | Editar evento |
| PATCH | `/:id/cancel` | Cancelar evento |
| PATCH | `/:id/status` | Cambiar estado (solo Admin) |

### Asistentes — `/api/attendees` *(requiere JWT)*
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/events/:id` | Ver asistentes de un evento |
| POST | `/events/:id/register` | Registrar asistente |
| PATCH | `/registrations/:id/cancel` | Cancelar inscripción |

### Admin — `/api/admin` *(requiere JWT + rol ADMIN)*
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/users` | Ver todos los usuarios |
| PUT | `/users/:id` | Editar usuario |
| DELETE | `/users/:id` | Eliminar usuario |
| GET | `/dashboard` | Estadísticas generales |

---

## 🐳 Correr con Docker

```powershell
docker-compose up --build
```

---

## 🧪 Correr tests

```powershell
pytest tests/
```
