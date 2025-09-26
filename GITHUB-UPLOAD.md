# 📤 Instrucciones para Subir el Repositorio a GitHub

Este documento contiene las instrucciones paso a paso para subir el proyecto Endurain al repositorio de GitHub.

## 🎯 Repositorio Destino
**URL**: `https://github.com/mausoftSistemas/enduraint`

## 📋 Prerrequisitos

1. **Git instalado** en tu sistema
2. **Cuenta de GitHub** con acceso al repositorio `mausoftSistemas/enduraint`
3. **Autenticación configurada** (SSH o Personal Access Token)

## 🚀 Pasos para Subir el Código

### 1. Inicializar Git (si no está inicializado)

```bash
cd "d:\WEBS\endurain-master\endurain-coach-student"
git init
```

### 2. Configurar el Repositorio Remoto

```bash
# Agregar el repositorio remoto
git remote add origin https://github.com/mausoftSistemas/enduraint.git

# Verificar que se agregó correctamente
git remote -v
```

### 3. Preparar Archivos para el Commit

```bash
# Agregar todos los archivos (excepto los del .gitignore)
git add .

# Verificar qué archivos se van a subir
git status
```

### 4. Crear el Primer Commit

```bash
# Crear commit inicial
git commit -m "🚀 Initial commit: Endurain sports training application

- FastAPI backend with PostgreSQL support
- Docker configuration for development and production
- EasyPanel deployment configuration
- Environment variables setup
- Complete project structure
- Authentication and security features
- Activity tracking and analysis
- Strava and Garmin integrations"
```

### 5. Subir al Repositorio

```bash
# Subir a la rama main
git push -u origin main
```

## 🔐 Configuración de Autenticación

### Opción A: Personal Access Token (Recomendado)

1. Ve a GitHub → Settings → Developer settings → Personal access tokens
2. Genera un nuevo token con permisos de `repo`
3. Usa el token como contraseña cuando Git te lo solicite

### Opción B: SSH Key

```bash
# Generar clave SSH (si no tienes una)
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"

# Agregar la clave al ssh-agent
ssh-add ~/.ssh/id_ed25519

# Copiar la clave pública y agregarla a GitHub
cat ~/.ssh/id_ed25519.pub
```

Luego cambiar la URL del repositorio:
```bash
git remote set-url origin git@github.com:mausoftSistemas/enduraint.git
```

## 📁 Archivos que se Subirán

### ✅ Archivos Incluidos
- `README.md` - Documentación principal
- `README-DEPLOYMENT.md` - Guía de despliegue
- `backend/` - Código del backend FastAPI
- `frontend/` - Código del frontend Vue.js
- `docker-compose.yml` - Configuración de desarrollo
- `docker-compose.prod.yml` - Configuración de producción
- `easypanel.yml` - Configuración para EasyPanel
- `.env.example` - Plantilla de variables de entorno
- `.gitignore` - Archivos a ignorar
- `backend/Dockerfile` - Imagen Docker del backend
- `backend/.dockerignore` - Archivos a ignorar en Docker

### ❌ Archivos Excluidos (por .gitignore)
- `.env` - Variables de entorno reales (contiene credenciales)
- `__pycache__/` - Cache de Python
- `node_modules/` - Dependencias de Node.js
- `*.log` - Archivos de log
- `.vscode/` - Configuración del IDE
- `data/` - Datos de la aplicación

## 🔍 Verificación Post-Subida

Después de subir el código, verifica:

1. **Repositorio en GitHub**: Ve a `https://github.com/mausoftSistemas/enduraint`
2. **Archivos presentes**: Confirma que todos los archivos están
3. **README visible**: El README.md debe mostrarse en la página principal
4. **Sin archivos sensibles**: Verifica que `.env` no esté presente

## 🛠️ Comandos de Mantenimiento

### Actualizar el Repositorio
```bash
# Agregar cambios
git add .

# Crear commit
git commit -m "Descripción de los cambios"

# Subir cambios
git push origin main
```

### Ver Estado del Repositorio
```bash
# Ver estado actual
git status

# Ver historial de commits
git log --oneline

# Ver diferencias
git diff
```

### Sincronizar con Cambios Remotos
```bash
# Descargar cambios del repositorio
git pull origin main
```

## 🚨 Solución de Problemas

### Error: "Repository not found"
- Verifica que tengas acceso al repositorio
- Confirma que la URL del repositorio es correcta
- Verifica tu autenticación (token o SSH)

### Error: "Permission denied"
- Verifica tus credenciales de GitHub
- Asegúrate de tener permisos de escritura en el repositorio
- Regenera tu Personal Access Token si es necesario

### Error: "Failed to push"
- Puede que el repositorio tenga cambios remotos
- Ejecuta `git pull origin main` primero
- Resuelve conflictos si los hay

### Archivos Grandes
Si tienes archivos muy grandes (>100MB):
```bash
# Instalar Git LFS
git lfs install

# Rastrear archivos grandes
git lfs track "*.zip"
git lfs track "*.tar.gz"

# Agregar .gitattributes
git add .gitattributes
```

## 📞 Contacto

Si tienes problemas con la subida del repositorio:
- Revisa la documentación de GitHub
- Contacta al administrador del repositorio
- Verifica los permisos de tu cuenta

---

**¡Listo para subir tu código a GitHub! 🚀**