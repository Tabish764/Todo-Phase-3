"""Error handling utilities for the Todo AI Chatbot application."""
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ChatBotError(HTTPException):
    """Base exception class for the chatbot application."""
    
    def __init__(
        self, 
        status_code: int, 
        error: str, 
        message: str, 
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail=ErrorResponse(
                error=error,
                message=message,
                details=details
            ).dict()
        )


class InvalidRequestError(ChatBotError):
    """Exception raised for invalid requests."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        details = {"field": field, "constraint": "validation"} if field else None
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error="INVALID_REQUEST",
            message=message,
            details=details
        )


class UnauthorizedError(ChatBotError):
    """Exception raised for unauthorized access."""
    
    def __init__(self, message: str = "User not found or unauthorized", field: str = "user_id"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error="UNAUTHORIZED",
            message=message,
            details={"field": field, "constraint": "exists"}
        )


class NotFoundError(ChatBotError):
    """Exception raised when a resource is not found."""
    
    def __init__(self, message: str, resource: str, resource_id: Optional[str] = None):
        details = {"field": resource, "constraint": "exists"}
        if resource_id:
            details["id"] = resource_id
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error="NOT_FOUND",
            message=message,
            details=details
        )


class ForbiddenError(ChatBotError):
    """Exception raised when access is forbidden."""
    
    def __init__(self, message: str, resource: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error="FORBIDDEN",
            message=message,
            details={"field": resource, "constraint": "user_access"}
        )


class ServiceUnavailableError(ChatBotError):
    """Exception raised when a service is unavailable."""
    
    def __init__(self, message: str, component: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error="SERVICE_UNAVAILABLE",
            message=message,
            details={"component": component, "reason": "unavailable"}
        )


class AIServiceError(ChatBotError):
    """Exception raised when AI service fails."""
    
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="AI_SERVICE_ERROR",
            message=message,
            details={"component": "ai_agent", "reason": "processing_failed"}
        )
