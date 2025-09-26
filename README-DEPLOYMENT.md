# 🚀 Guía de Despliegue - Endurain Backend en EasyPanel

Esta guía te ayudará a desplegar el backend de Endurain en EasyPanel de manera rápida y segura.

## 📋 Prerrequisitos

1. Cuenta en EasyPanel
2. Repositorio Git con el código (GitHub, GitLab, etc.)
3. Conocimientos básicos de Docker y variables de entorno

## 🔧 Configuración Inicial

### 1. Preparar el Repositorio

Asegúrate de que tu repositorio contenga los siguientes archivos:
- `backend/Dockerfile`
- `backend/.dockerignore`
- `docker-compose.yml` (para desarrollo local)
- `docker-compose.prod.yml` (para producción)
- `.env.example`
- `easypanel.yml`

### 2. Variables de Entorno Obligatorias

Antes de desplegar, necesitas generar las siguientes claves de seguridad:

#### Generar SECRET_KEY
```bash
openssl rand -hex 32
```

#### Generar FERNET_KEY
```python
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 🚀 Despliegue en EasyPanel

### Opción 1: Usando la Interfaz Web de EasyPanel

1. **Crear Nueva Aplicación**
   - Ve a tu dashboard de EasyPanel
   - Haz clic en "New Service" → "App"
   - Selecciona "From Source Code"

2. **Configurar el Repositorio**
   - Repository URL: `https://github.com/tu-usuario/endurain-coach-student`
   - Branch: `main`
   - Build Path: `/backend`
   - Dockerfile: `Dockerfile`

3. **Configurar Variables de Entorno**
   ```
   DB_TYPE=postgres
   DB_HOST=[IP_DE_TU_POSTGRES]
   DB_PORT=5432
   DB_DATABASE=endurain
   DB_USER=endurain
   DB_PASSWORD=[TU_PASSWORD_POSTGRES]
   SECRET_KEY=[TU_SECRET_KEY_GENERADA]
   FERNET_KEY=[TU_FERNET_KEY_GENERADA]
   ENDURAIN_HOST=https://tu-dominio.com
   ENVIRONMENT=production
   TZ=UTC
   ```

4. **Configurar Base de Datos PostgreSQL**
   - Crear un servicio PostgreSQL en EasyPanel
   - Versión recomendada: PostgreSQL 15
   - Configurar usuario: `endurain`
   - Configurar base de datos: `endurain`

5. **Configurar Volúmenes**
   - `/app/data` → 10GB (para archivos de actividades)
   - `/app/logs` → 1GB (para logs)

6. **Configurar Dominio**
   - Asignar dominio personalizado
   - Configurar SSL/TLS automático

### Opción 2: Usando Docker Compose (Desarrollo Local)

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/endurain-coach-student.git
cd endurain-coach-student

# Copiar y configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend
```

### Opción 3: Solo Backend en Producción

```bash
# Usar el docker-compose de producción
docker-compose -f docker-compose.prod.yml up -d
```

## 🔒 Configuración de Seguridad

### Variables de Entorno Críticas

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave para JWT | `a1b2c3d4e5f6...` |
| `FERNET_KEY` | Clave para encriptación | `abcdefghijklmnop...` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `mi_password_seguro` |

### Configuración SMTP (Opcional)

Para funcionalidad de reset de contraseñas:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
SMTP_USE_TLS=true
```

## 🔍 Verificación del Despliegue

### 1. Health Check
```bash
curl https://tu-dominio.com/api/v1/health
```

### 2. Verificar Base de Datos
```bash
curl https://tu-dominio.com/api/v1/users/me
```

### 3. Ver Logs
En EasyPanel, ve a tu aplicación → Logs

## 🐛 Solución de Problemas

### Error: "Missing required environment variable"
- Verifica que todas las variables obligatorias estén configuradas
- Revisa el archivo `.env.example` para la lista completa

### Error de Conexión a Base de Datos
- Verifica que PostgreSQL esté ejecutándose
- Confirma las credenciales de conexión
- Revisa que el host y puerto sean correctos

### Error 500 en la API
- Revisa los logs de la aplicación
- Verifica que las migraciones de Alembic se ejecutaron correctamente

### Problemas de Permisos en Volúmenes
```bash
# En el contenedor
chown -R 1000:1000 /app/data
chown -R 1000:1000 /app/logs
```

## 📊 Monitoreo y Mantenimiento

### Logs Importantes
- `/app/logs/` - Logs de la aplicación
- Logs de PostgreSQL en EasyPanel
- Logs del contenedor Docker

### Backup de Base de Datos
```bash
# Crear backup
pg_dump -h [DB_HOST] -U endurain -d endurain > backup.sql

# Restaurar backup
psql -h [DB_HOST] -U endurain -d endurain < backup.sql
```

### Actualización de la Aplicación
1. Push cambios al repositorio
2. En EasyPanel: Rebuild & Deploy
3. Verificar que todo funcione correctamente

## 🔗 Enlaces Útiles

- [Documentación de EasyPanel](https://easypanel.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

## 📞 Soporte

Si encuentras problemas durante el despliegue:
1. Revisa los logs detalladamente
2. Verifica la configuración de variables de entorno
3. Consulta la documentación oficial de EasyPanel
4. Crea un issue en el repositorio del proyecto

---

¡Tu backend de Endurain debería estar funcionando correctamente en EasyPanel! 🎉