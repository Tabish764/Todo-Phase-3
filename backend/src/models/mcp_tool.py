"""
MCP Tool Base Model

This module defines the base models for MCP tools.
"""
from pydantic import BaseModel
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class MCPToolBase(ABC):
    """Abstract base class for MCP tools"""

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the MCP tool with given input data"""
        pass

    @abstractmethod
    def get_input_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's input"""
        pass

    @abstractmethod
    def get_output_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's output"""
        pass


class MCPInputBase(BaseModel):
    """Base class for MCP tool inputs"""
    user_id: str


class MCPOutputBase(BaseModel):
    """Base class for MCP tool outputs"""
    status: str


class AddTaskInput(MCPInputBase):
    """Input model for add_task tool"""
    title: str
    description: Optional[str] = None


class AddTaskOutput(MCPOutputBase):
    """Output model for add_task tool"""
    task_id: int
    title: str
    description: Optional[str] = None


class ListTasksInput(MCPInputBase):
    """Input model for list_tasks tool"""
    status: Optional[str] = "all"  # "all", "pending", "completed"


class TaskItem(BaseModel):
    """Model for individual task items in list_tasks output"""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: str
    updated_at: str


class ListTasksOutput(MCPOutputBase):
    """Output model for list_tasks tool"""
    tasks: list[TaskItem]
    count: int


class CompleteTaskInput(MCPInputBase):
    """Input model for complete_task tool"""
    task_id: int


class CompleteTaskOutput(MCPOutputBase):
    """Output model for complete_task tool"""
    task_id: int
    title: str


class DeleteTaskInput(MCPInputBase):
    """Input model for delete_task tool"""
    task_id: int


class DeleteTaskOutput(MCPOutputBase):
    """Output model for delete_task tool"""
    task_id: int
    title: str


class UpdateTaskInput(MCPInputBase):
    """Input model for update_task tool"""
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None


class UpdateTaskOutput(MCPOutputBase):
    """Output model for update_task tool"""
    task_id: int
    title: str
    description: Optional[str] = None