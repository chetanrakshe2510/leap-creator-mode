"""
FastAPI application package.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env files
def load_env_files():
    """Load environment variables from .env files in both root and backend directories."""
    # Get the project root directory (parent of backend)
    root_dir = Path(__file__).parent.parent.parent.parent
    backend_dir = root_dir / "backend"
    
    # Try to load from root .env first
    root_env = root_dir / ".env"
    if root_env.exists():
        logger.info(f"Loading environment variables from {root_env}")
        load_dotenv(dotenv_path=root_env)
    
    # Then try to load from backend .env (will override if same variables)
    backend_env = backend_dir / ".env"
    if backend_env.exists():
        logger.info(f"Loading environment variables from {backend_env}")
        load_dotenv(dotenv_path=backend_env)
    
    # Log loaded environment variables (without values for security)
    env_vars = [
        "SUPABASE_URL", 
        "SUPABASE_KEY", 
        "SENDGRID_API_KEY", 
        "NOTIFICATION_EMAIL_FROM",
        "OPENAI_API_KEY",
        "USE_SUPABASE_STORAGE",
        "SUPABASE_STORAGE_BUCKET",
        "BASE_URL"
    ]
    
    for var in env_vars:
        if os.environ.get(var):
            logger.info(f"Environment variable loaded: {var}")
        else:
            logger.warning(f"Environment variable not found: {var}")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Load environment variables
    load_env_files()
    
    app = FastAPI(
        title="AskLeap API",
        description="API for generating educational animations using Manim",
        version="0.1.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    from .routes import animations, feedback, system
    app.include_router(animations.router, prefix="/api/animations", tags=["animations"])
    app.include_router(feedback.router, prefix="/api", tags=["feedback"])
    app.include_router(system.router, prefix="/api/system", tags=["system"])
    
    # Serve videos directory as static files
    videos_dir = Path(__file__).parent.parent.parent / "generated" / "media" / "videos"
    if videos_dir.exists():
        logger.info(f"Serving videos from: {videos_dir}")
        app.mount("/videos", StaticFiles(directory=str(videos_dir)), name="videos")
    else:
        logger.warning(f"Videos directory not found at {videos_dir}")
        # Create the directory
        videos_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created videos directory at: {videos_dir}")
        app.mount("/videos", StaticFiles(directory=str(videos_dir)), name="videos")
    
    # Serve frontend static files
    # Look for the frontend build directory
    frontend_build_dir = Path("/app/frontend/dist")
    
    if frontend_build_dir.exists():
        logger.info(f"Serving frontend from: {frontend_build_dir}")
        app.mount("/", StaticFiles(directory=str(frontend_build_dir), html=True), name="frontend")
    else:
        # Try relative path for local development
        local_frontend_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "dist"
        if local_frontend_dir.exists():
            logger.info(f"Serving frontend from local path: {local_frontend_dir}")
            app.mount("/", StaticFiles(directory=str(local_frontend_dir), html=True), name="frontend")
        else:
            logger.warning(f"Frontend build directory not found at {frontend_build_dir} or {local_frontend_dir}")
            logger.warning("Make sure to build the frontend with 'npm run build' in the frontend directory")
    
    return app
