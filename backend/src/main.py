import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints.tasks import router as tasks_router
from src.database.connection import db_connection

# -----------------------------
# Logging configuration
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Lifespan context for startup/shutdown
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    logger.info("Starting up application...")
    try:
        # Connect to database
        await db_connection.connect()
        logger.info("Database connection established")

        # Optionally create tables
        try:
            from sqlmodel import SQLModel
            async with db_connection.engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database tables created/verified")
        except Exception as table_error:
            logger.warning(f"Could not create tables: {str(table_error)}")
            logger.info("Continuing without table creation - ensure tables exist")

        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    finally:
        logger.info("Shutting down application...")
        await db_connection.disconnect()
        logger.info("Database connection closed")

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(
    title="Task Backend API",
    description="Backend API for task management frontend integration",
    version="1.0.0",
    lifespan=lifespan
)

# -----------------------------
# CORS configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://todo-phase-ii.vercel.app",  # Frontend origin(s)
        # Add other origins if needed
    ],
    allow_credentials=True,  # Required for cookies or auth headers
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include routers
# -----------------------------
app.include_router(tasks_router)

# -----------------------------
# Root endpoint
# -----------------------------
@app.get("/")
async def root():
    return {"message": "Task Backend API"}

# -----------------------------
# Health check endpoint
# -----------------------------
@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    try:
        from sqlmodel import select
        from src.database.models import Task
        from src.database.session import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            stmt = select(Task).limit(1)
            result = await session.execute(stmt)
            _ = result.scalar_one_or_none()

        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}