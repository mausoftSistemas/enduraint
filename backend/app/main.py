import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from alembic.config import Config
from alembic import command

from app.core import logger as core_logger
from app.core import config as core_config
from app.core import scheduler as core_scheduler
from app.core import tracing as core_tracing
from app.core import migrations as core_migrations

from app.garmin import activity_utils as garmin_activity_utils
from app.garmin import health_utils as garmin_health_utils

from app.session import schema as session_schema

from app.strava import activity_utils as strava_activity_utils
from app.strava import utils as strava_utils

from app.password_reset_tokens import utils as password_reset_tokens_utils

from app.core.routes import router as api_router


async def startup_event():
    core_logger.print_to_log_and_console(
        f"Backend startup event - {core_config.API_VERSION}"
    )

    # Run Alembic migrations to ensure the database is up to date
    alembic_cfg = Config("alembic.ini")
    # Disable the logger configuration in Alembic to avoid conflicts with FastAPI
    alembic_cfg.attributes["configure_logger"] = False
    command.upgrade(alembic_cfg, "head")

    # Migration check
    core_migrations.check_migrations()

    # Create a scheduler to run background jobs
    core_scheduler.start_scheduler()

    # Retrieve last day activities from Garmin Connect and Strava
    core_logger.print_to_log_and_console(
        "Refreshing Strava tokens on startup on startup"
    )
    strava_utils.refresh_strava_tokens(True)

    # Retrieve last day activities from Garmin Connect and Strava
    core_logger.print_to_log_and_console(
        "Retrieving last day activities from Garmin Connect and Strava on startup"
    )
    await garmin_activity_utils.retrieve_garminconnect_users_activities_for_days(1)
    await strava_activity_utils.retrieve_strava_users_activities_for_days(1, True)

    # Retrieve last day body composition from Garmin Connect
    core_logger.print_to_log_and_console(
        "Retrieving last day body composition from Garmin Connect on startup"
    )
    garmin_health_utils.retrieve_garminconnect_users_bc_for_days(1)

    # Delete invalid password reset tokens
    core_logger.print_to_log_and_console(
        "Deleting invalid password reset tokens from the database"
    )
    password_reset_tokens_utils.delete_invalid_tokens_from_db()


def shutdown_event():
    # Log the shutdown event
    core_logger.print_to_log_and_console("Backend shutdown event")

    # Shutdown the scheduler when the application is shutting down
    core_scheduler.stop_scheduler()


def create_app() -> FastAPI:
    # Define the FastAPI object
    app = FastAPI(
        docs_url=core_config.ROOT_PATH + "/docs",
        redoc_url=core_config.ROOT_PATH + "/redoc",
        title="Endurain",
        summary="Endurain API for the Endurain app",
        version=core_config.API_VERSION,
        license_info={
            "name": core_config.LICENSE_NAME,
            "identifier": core_config.LICENSE_IDENTIFIER,
            "url": core_config.LICENSE_URL,
        },
    )

    # Add CORS middleware to allow requests from the frontend
    origins = [
        "http://localhost:8080",
        "http://localhost:5173",
        os.environ.get("ENDURAIN_HOST"),
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=(
            origins
            if core_config.ENVIRONMENT == "development"
            else os.environ.get("ENDURAIN_HOST")
        ),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(session_schema.CSRFMiddleware)

    # Router files
    app.include_router(api_router)

    # Add a route to serve the user images
    app.mount(
        f"/{core_config.USER_IMAGES_DIR}",
        StaticFiles(directory=core_config.USER_IMAGES_DIR),
        name="user_images",
    )
    app.mount(
        f"/{core_config.SERVER_IMAGES_DIR}",
        StaticFiles(directory=core_config.SERVER_IMAGES_DIR),
        name="server_images",
    )
    app.mount(
        f"/{core_config.ACTIVITY_MEDIA_DIR}",
        StaticFiles(directory=core_config.ACTIVITY_MEDIA_DIR),
        name="activity_media",
    )
    app.mount(
        "/", StaticFiles(directory=core_config.FRONTEND_DIR, html=True), name="frontend"
    )

    return app


# Silence stravalib token warnings
os.environ["SILENCE_TOKEN_WARNINGS"] = "TRUE"

# Check for required environment variables
core_config.check_required_env_vars()

# Check for required directories
core_config.check_required_dirs()

# Create the FastAPI application
app = create_app()

# Create logggers
core_logger.setup_main_logger()

# Setup tracing
core_tracing.setup_tracing(app)

# Register the startup event handler
app.add_event_handler("startup", startup_event)

# Register the shutdown event handler
app.add_event_handler("shutdown", shutdown_event)