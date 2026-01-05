"""ToolCall model for the Todo AI Chatbot application."""
from typing import Dict, Any
from pydantic import BaseModel


class ToolCall(BaseModel):
    """Model for MCP tool calls embedded in messages."""
    tool_name: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]


class ToolCallRecord(BaseModel):
    """Model for recording tool call execution."""
    name: str
    args: Dict[str, Any]
    result: Dict[str, Any]
    timestamp: str
