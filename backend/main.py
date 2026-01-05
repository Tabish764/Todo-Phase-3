"""Main application entry point for the Todo AI Chatbot."""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.src.database.engine import async_engine
from backend.src.api.v1.chat_router import router as chat_router
from backend.config import settings
from sqlmodel import SQLModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting up the application...")
    
    # Initialize database
    async with async_engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(SQLModel.metadata.create_all)
    
    logger.info("Database tables created/verified")
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("Shutting down the application...")
    await async_engine.dispose()


# Create FastAPI app
app = FastAPI(
    title="Todo AI Chatbot API",
    description="API for the Todo AI Chatbot application",
    version="1.0.0",
    lifespan=lifespan
)


# Include routers
app.include_router(chat_router)


@app.get("/")
def read_root():
    """Root endpoint for health check."""
    return {"message": "Todo AI Chatbot API is running!"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "api": "todo-ai-chatbot"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
