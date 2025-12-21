import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints.tasks import router as tasks_router
from src.database.connection import db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to handle startup and shutdown events"""
    logger.info("Starting up application...")
    try:
        # Initialize database connection
        await db_connection.connect()
        logger.info("Database connection established")

        # Optionally create tables if they don't exist
        # This may fail if the database is not accessible, but we don't want to crash the app
        try:
            from sqlmodel import SQLModel
            async with db_connection.engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database tables created/verified")
        except Exception as table_error:
            logger.warning(f"Could not create tables during startup: {str(table_error)}")
            logger.info("Application will continue without table creation - ensure tables exist")

        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    finally:
        logger.info("Shutting down application...")
        # Close database connection
        await db_connection.disconnect()
        logger.info("Database connection closed")


app = FastAPI(
    title="Task Backend API",
    description="Backend API for task management frontend integration",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Allow credentials to be included in cross-origin requests
    # This is necessary for session cookies to be sent with API requests
)

# Include API routers
app.include_router(tasks_router)


@app.get("/")
async def root():
    return {"message": "Task Backend API"}


@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running"""
    logger.info("Health check endpoint accessed")
    try:
        # Check database connectivity
        from sqlmodel import select
        from src.database.models import Task
        from src.database.session import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            # Try to query something lightweight
            stmt = select(Task).limit(1)
            result = await session.execute(stmt)
            _ = result.scalar_one_or_none()

        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}