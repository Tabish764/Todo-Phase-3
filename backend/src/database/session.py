from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from .connection import db_connection


# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    bind=db_connection.engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db_session():
    """Dependency to get database session for FastAPI endpoints"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()