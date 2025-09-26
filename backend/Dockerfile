# Dockerfile para Endurain Backend
FROM python:3.12-slim

# Instalar dependencias del sistema necesarias para las librerías de Python
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libmariadb-dev \
    libpq-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install poetry

# Configurar Poetry para no crear entornos virtuales (ya estamos en un contenedor)
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VIRTUALENVS_CREATE=false

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración de Poetry
COPY pyproject.toml poetry.lock ./

# Instalar dependencias
RUN poetry install --only=main --no-root && rm -rf $POETRY_CACHE_DIR

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/backend/data/user_images \
    /app/backend/data/server_images \
    /app/backend/data/activity_files \
    /app/backend/data/activity_media \
    /app/backend/logs

# Establecer variables de entorno por defecto
ENV PYTHONPATH=/app \
    BACKEND_DIR=/app \
    DATA_DIR=/app/data \
    LOGS_DIR=/app/logs \
    FILES_DIR=/app/data/activity_files \
    ACTIVITY_MEDIA_DIR=/app/data/activity_media \
    ENVIRONMENT=production

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]