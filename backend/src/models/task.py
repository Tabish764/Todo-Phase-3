from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, DateTime, Boolean, Integer

class Task(SQLModel, table=True):
    """Task model for database storage - maps to 'task' table in Neon"""
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)

    # Use sa_column to explicitly map to camelCase 'userId'
    userid: str = Field(
        sa_column=Column("userId", String, index=True, nullable=False)
    )

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)

    # Use sa_column to explicitly map to camelCase 'createdAt'
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column("createdAt", DateTime(timezone=True))
    )

    # Use sa_column to explicitly map to camelCase 'updatedAt'
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "updatedAt", 
            DateTime(timezone=True), 
            onupdate=lambda: datetime.now(timezone.utc)
        )
    )