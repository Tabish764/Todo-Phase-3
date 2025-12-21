from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
import sqlalchemy as sa
from pydantic import BaseModel, field_validator


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(sa_column=Column(sa.Text, primary_key=True))
    email: str = Field(sa_column=Column(sa.Text, unique=True, nullable=False))
    email_verified: bool = Field(sa_column=Column("emailVerified", sa.Boolean, default=False))
    name: Optional[str] = Field(sa_column=Column(sa.Text), default=None)
    image: Optional[str] = Field(sa_column=Column(sa.Text), default=None)
    password: Optional[str] = Field(sa_column=Column(sa.Text), default=None)  # For email/password auth
    created_at: datetime = Field(sa_column=Column("createdAt", sa.DateTime, nullable=False), default_factory=datetime.now)
    updated_at: datetime = Field(sa_column=Column("updatedAt", sa.DateTime, nullable=False), default_factory=datetime.now)


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: str = Field(sa_column=Column(sa.Text, primary_key=True))
    user_id: str = Field(sa_column=Column("userId", sa.Text, nullable=False))  # Index will be added via table_args if needed
    expires_at: datetime = Field(sa_column=Column("expiresAt", sa.DateTime, nullable=False))
    token: str = Field(sa_column=Column(sa.Text, unique=True, nullable=False))  # The session token
    ip_address: Optional[str] = Field(sa_column=Column("ipAddress", sa.Text), default=None)
    user_agent: Optional[str] = Field(sa_column=Column("userAgent", sa.Text), default=None)
    created_at: datetime = Field(sa_column=Column("createdAt", sa.DateTime, nullable=False), default_factory=datetime.now)
    updated_at: datetime = Field(sa_column=Column("updatedAt", sa.DateTime, nullable=False), default_factory=datetime.now)

    # Add index via table_args
    __table_args__ = (sa.Index('idx_session_user_id', 'userId'), sa.Index('idx_session_token', 'token', unique=True))


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

    @field_validator('title')
    def validate_title(cls, v):
        if not v or len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    # Map Python's user_id to the database column "userId" (camelCase)
    user_id: str = Field(sa_column=Column("userId", sa.Text, nullable=False))
    created_at: datetime = Field(sa_column=Column("createdAt", sa.DateTime, nullable=False), default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column("updatedAt", sa.DateTime, nullable=False))

    # Add index on the actual DB column name "userId"
    __table_args__ = (sa.Index("idx_task_user_id", "userId"),)


class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None

    @field_validator('title')
    def validate_title(cls, v):
        if not v or len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator('title')
    def validate_title(cls, v):
        if v is not None and (len(v) < 1 or len(v) > 200):
            raise ValueError('Title must be between 1 and 200 characters')
        return v


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime


class ErrorResponse(BaseModel):
    error: str