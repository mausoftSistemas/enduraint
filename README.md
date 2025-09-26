# 🏃‍♂️ Endurain - Aplicación de Entrenamiento Deportivo

**Endurain** es una aplicación completa para el seguimiento y análisis de actividades deportivas, diseñada para entrenadores y atletas que buscan optimizar su rendimiento.

## 🌟 Características Principales

- 📊 **Análisis de Actividades**: Procesamiento de archivos GPX, TCX y FIT
- 🗺️ **Mapas Interactivos**: Visualización de rutas con geocoding
- 👥 **Gestión de Entrenadores y Estudiantes**: Sistema completo de roles
- 🔗 **Integraciones**: Strava y Garmin Connect
- 📱 **API REST**: Backend completo con FastAPI
- 🎯 **Objetivos y Metas**: Seguimiento de progreso personalizado
- 📧 **Notificaciones**: Sistema de alertas y comunicación
- 🔐 **Seguridad**: Autenticación JWT y encriptación

## 🏗️ Arquitectura

### Backend (FastAPI)
- **Framework**: FastAPI con Python 3.12
- **Base de Datos**: PostgreSQL con SQLAlchemy
- **Migraciones**: Alembic
- **Autenticación**: JWT con bcrypt
- **Contenedores**: Docker y Docker Compose

### Frontend (Vue.js)
- **Framework**: Vue.js 3 con Vite
- **UI**: Componentes modernos y responsivos
- **Estado**: Gestión centralizada
- **Mapas**: Integración con servicios de mapas

## 🚀 Despliegue Rápido

### Usando Docker Compose (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/mausoftSistemas/enduraint.git
cd enduraint

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend
```

### Despliegue en EasyPanel

1. **Crear servicio PostgreSQL** en EasyPanel
2. **Crear aplicación** desde este repositorio
3. **Configurar variables de entorno** (ver `.env.example`)
4. **Configurar volúmenes** para persistencia de datos

Ver [README-DEPLOYMENT.md](./README-DEPLOYMENT.md) para instrucciones detalladas.

## ⚙️ Configuración

### Variables de Entorno Principales

```env
# Base de datos
DB_TYPE=postgres
DB_HOST=tu-host-postgres
DB_DATABASE=endurain
DB_USER=tu-usuario
DB_PASSWORD=tu-password

# Seguridad (CAMBIAR EN PRODUCCIÓN)
SECRET_KEY=tu-clave-secreta-jwt
FERNET_KEY=tu-clave-fernet

# Aplicación
ENDURAIN_HOST=https://tu-dominio.com
ENVIRONMENT=production
```

### Generar Claves de Seguridad

```bash
# SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# FERNET_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 🛠️ Desarrollo Local

### Prerrequisitos
- Python 3.12+
- Poetry
- PostgreSQL
- Node.js 18+

### Backend
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend/app
npm install
npm run dev
```

## 📁 Estructura del Proyecto

```
endurain/
├── backend/                 # API FastAPI
│   ├── app/                # Código de la aplicación
│   │   ├── activities/     # Gestión de actividades
│   │   ├── users/          # Gestión de usuarios
│   │   ├── core/           # Configuración central
│   │   └── ...
│   ├── alembic/            # Migraciones de BD
│   ├── Dockerfile          # Imagen Docker
│   └── pyproject.toml      # Dependencias Python
├── frontend/               # Aplicación Vue.js
│   └── app/
│       ├── src/            # Código fuente
│       ├── public/         # Archivos estáticos
│       └── package.json    # Dependencias Node.js
├── docker-compose.yml      # Desarrollo local
├── docker-compose.prod.yml # Producción
└── easypanel.yml          # Configuración EasyPanel
```

## 🔌 API Endpoints

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/register` - Registrar usuario
- `POST /api/v1/auth/refresh` - Renovar token

### Actividades
- `GET /api/v1/activities` - Listar actividades
- `POST /api/v1/activities` - Crear actividad
- `GET /api/v1/activities/{id}` - Obtener actividad
- `PUT /api/v1/activities/{id}` - Actualizar actividad

### Usuarios
- `GET /api/v1/users/me` - Perfil actual
- `PUT /api/v1/users/me` - Actualizar perfil
- `GET /api/v1/users/{id}` - Obtener usuario

Ver documentación completa en `/docs` (Swagger UI)

## 🧪 Testing

```bash
# Backend
cd backend
poetry run pytest

# Frontend
cd frontend/app
npm run test
```

## 📊 Monitoreo

- **Health Check**: `/api/v1/health`
- **Métricas**: Integración con Jaeger (opcional)
- **Logs**: Centralizados en `/app/logs`

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia AGPL-3.0. Ver [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

- **Documentación**: [README-DEPLOYMENT.md](./README-DEPLOYMENT.md)
- **Issues**: [GitHub Issues](https://github.com/mausoftSistemas/enduraint/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/mausoftSistemas/enduraint/discussions)

## 🏆 Créditos

Desarrollado con ❤️ por el equipo de **MauSoft Sistemas**.

---

**¡Comienza tu viaje de entrenamiento con Endurain! 🚀**