import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Simplified imports - avoiding problematic dependencies
try:
    import core.logger as core_logger
except ImportError:
    core_logger = None

try:
    import core.config as core_config
except ImportError:
    core_config = None

# Import basic routers that should work
try:
    from users.user.router import router as user_router
except ImportError:
    user_router = None

try:
    from session.router import router as session_router
except ImportError:
    session_router = None

try:
    from coaches.router import router as coaches_router
except ImportError:
    coaches_router = None

try:
    from students.router import router as students_router
except ImportError:
    students_router = None

def create_app() -> FastAPI:
    app = FastAPI(
        title="Endurain Coach-Student API",
        description="API for Endurain Coach-Student system",
        version="0.14.0",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add routers if available
    if user_router:
        app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
    if session_router:
        app.include_router(session_router, prefix="/api/v1/session", tags=["session"])
    if coaches_router:
        app.include_router(coaches_router, prefix="/api/v1/coaches", tags=["coaches"])
    if students_router:
        app.include_router(students_router, prefix="/api/v1/students", tags=["students"])

    @app.get("/")
    async def root():
        return {"message": "Endurain Coach-Student API is running"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": "0.14.0"}

    return app

# Create the app
app = create_app()

# Setup logger if available
if core_logger:
    try:
        core_logger.setup_main_logger()
    except Exception as e:
        print(f"Warning: Could not setup logger: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)