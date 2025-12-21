from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


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