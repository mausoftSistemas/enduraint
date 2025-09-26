FROM python:3.12-slim
# Configurar variables de entorno para optimizar el build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema en una sola capa optimizada
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libmariadb-dev \
    libpq-dev \
    pkg-config \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry==1.8.3

# Configurar Poetry para no crear entornos virtuales
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VIRTUALENVS_CREATE=false

# Establecer directorio de trabajo
WORKDIR /app

# Copiar solo archivos de dependencias primero (mejor caching)
COPY pyproject.toml poetry.lock ./

# Instalar dependencias en una capa separada para mejor caching
RUN poetry install --only=main --no-root --no-dev \
    && rm -rf $POETRY_CACHE_DIR \
    && poetry cache clear pypi --all

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios y establecer permisos en una sola capa
RUN mkdir -p \
    /app/data/user_images \
    /app/data/server_images \
    /app/data/activity_files \
    /app/data/activity_media \
    /app/logs \
    && chmod -R 755 /app/data /app/logs

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

# Usar un usuario no-root para mayor seguridad
RUN groupadd -r endurain && useradd -r -g endurain endurain \
    && chown -R endurain:endurain /app
USER endurain

# Comando de inicio optimizado
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]