"""Database session management for the Todo AI Chatbot application."""
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import Depends
from .engine import async_engine


@asynccontextmanager
async def get_session_context(engine: AsyncEngine = async_engine) -> AsyncGenerator[AsyncSession, None]:
    """Get database session with automatic cleanup."""
    async with AsyncSession(engine) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session for dependency injection."""
    async with AsyncSession(async_engine) as session:
        yield session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency for FastAPI."""
    async with AsyncSession(async_engine) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
