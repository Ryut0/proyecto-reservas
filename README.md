# Sistema de Reservas Deportivas (Django + DRF)

Proyecto completo para gestionar reservas de canchas deportivas usando Django 4.x y Django REST Framework.

## Requisitos

- Python 3.10+
- PostgreSQL (Supabase) 
- pip

## Instalación

1. Crear y activar entorno virtual
2. Instalar dependencias

```bash
pip install -r requirements.txt
```

3. Crear archivo `.env` en la raíz del proyecto

## Paso a paso (al clonar en VS Code)

1. Clonar el repositorio y abrir la carpeta en VS Code
2. Crear y activar el entorno virtual

```bash
python -m venv env
```

Windows:
```bash
env\\Scripts\\activate
```

Mac/Linux:
```bash
source env/bin/activate
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

4. Crear el archivo `.env` en la raíz (usa `.env.example` como base)

5. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Levantar el servidor

```bash
python manage.py runserver
```

7. Abrir en el navegador

- `http://127.0.0.1:8000/`

## Configuración `.env`

Ejemplo recomendado:

```env
DJANGO_SECRET_KEY=tu-clave-secreta
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=postgresql://postgres:tu_password@aws-1-us-east-1.pooler.supabase.com:5432/postgres

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=tu-host.supabase.co
DB_PORT=5432
```

Si no configuras PostgreSQL, el proyecto usará SQLite por defecto para desarrollo.

## Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## Ejecutar servidor

```bash
python manage.py runserver
```

## Endpoints API

Base URL: `/api/`

- `GET /api/clientes/`
- `POST /api/clientes/`
- `GET /api/clientes/{id}/`
- `PUT/PATCH /api/clientes/{id}/`
- `DELETE /api/clientes/{id}/`

- `GET /api/canchas/`
- `POST /api/canchas/`
- `GET /api/canchas/{id}/`
- `PUT/PATCH /api/canchas/{id}/`
- `DELETE /api/canchas/{id}/`

- `GET /api/reservas/` (protegido)
- `POST /api/reservas/` (protegido)
- `GET /api/reservas/{id}/` (protegido)
- `PUT/PATCH /api/reservas/{id}/` (protegido)
- `DELETE /api/reservas/{id}/` (protegido)

Autenticación:

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/` (protegido)

## Frontend (Templates)

Rutas principales:

- `/` Lista de canchas
- `/reservas/` Lista de reservas (requiere token)
- `/reservas/nueva/` Formulario de reserva (requiere token)

El frontend consume la API usando `fetch()` y Bootstrap.

## Regla de negocio

Una cancha no puede tener dos reservas en el mismo horario. La validación se realiza en el serializer de `Reserva`:

- `hora_inicio < hora_fin`
- No hay reservas en el mismo día y cancha
