"""Error response models for the Todo AI Chatbot application."""
from typing import Optional, Dict, Any
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Model for error details."""
    field: Optional[str] = None
    constraint: Optional[str] = None
    id: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
