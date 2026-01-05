import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from src.api.v1.endpoints.tasks import router as tasks_router
from src.api.v1.chat_router import router as chat_router
from src.api.v1.conversation_router import router as conversation_router
from src.api.v1.mcp_router import router as mcp_router
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

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(
    title="Task Backend API",
    description="Backend API for task management frontend integration",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limit handler to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# -----------------------------
# CORS configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000","https://todo-phase-3.vercel.app"  # Frontend origin(s)
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
app.include_router(chat_router, prefix="/api")  # Register chat router with /api prefix
app.include_router(conversation_router)  # Conversation router at root level, like tasks
app.include_router(mcp_router, prefix="/api/v1")

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
        from src.database.session import get_db_session

        # Use the get_db_session dependency to get a session
        async for session in get_db_session():
            stmt = select(Task).limit(1)
            result = await session.execute(stmt)
            _ = result.scalar_one_or_none()
            break  # We only need one session from the generator

        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}