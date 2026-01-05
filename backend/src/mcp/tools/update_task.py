"""
Update Task Tool Implementation

This module implements the update_task tool for the MCP server.
"""
import json
from typing import Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.mcp_tool import UpdateTaskInput, UpdateTaskOutput, MCPToolBase
from src.services.mcp_service import TaskMCPService
from src.utils.validation import validate_update_task_input
from src.utils.auth import verify_user_owns_task


class UpdateTaskTool(MCPToolBase):
    """Implementation of the update_task MCP tool"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the update_task tool with given input data"""
        # Validate input
        is_valid, error_msg = validate_update_task_input(input_data)
        if not is_valid:
            return {
                "status": "error",
                "error": error_msg
            }

        # Extract input values
        user_id = input_data["user_id"]
        task_id_input = input_data["task_id"]
        title = input_data.get("title")
        description = input_data.get("description")

        # Convert integer task_id to UUID if needed
        from uuid import UUID
        from src.database.models import Task
        
        # Handle both integer (from spec) and UUID string inputs
        if isinstance(task_id_input, int):
            # Search for task by converting UUIDs to integers
            stmt = select(Task).where(Task.user_id == user_id)
            result = await self.db_session.exec(stmt)
            all_tasks = result.all()
            
            task = None
            for t in all_tasks:
                task_id_int = int(str(t.id).replace('-', '')[:12], 16) % (10**9)
                if task_id_int == task_id_input:
                    task = t
                    break
            
            if not task:
                return {
                    "status": "error",
                    "error": "Task not found"
                }
            task_id = task.id
        else:
            # Assume it's a UUID string
            try:
                task_id = UUID(task_id_input) if isinstance(task_id_input, str) else task_id_input
            except (ValueError, AttributeError):
                return {
                    "status": "error",
                    "error": f"Invalid task_id format: {task_id_input}"
                }
            
            # Get the task to check if it exists
            stmt = select(Task).where(Task.id == task_id)
            result = await self.db_session.exec(stmt)
            task = result.first()

        # Verify user owns the task
        user_owns_task = await verify_user_owns_task(self.db_session, user_id, task_id)
        if not user_owns_task:
            return {
                "status": "error",
                "error": "Unauthorized"
            }

        # Update task using the service
        service = TaskMCPService(self.db_session)
        try:

            if not task:
                return {
                    "status": "error",
                    "error": "Task not found"
                }

            # Update task details
            updated_task = await service.update_task_details(
                task_id, user_id, title, description
            )

            if updated_task:
                # Convert UUID to integer for spec compliance
                task_id_int = int(str(updated_task.id).replace('-', '')[:12], 16) % (10**9)
                
                # Return success response matching spec: {task_id, status, title}
                return {
                    "task_id": task_id_int,
                    "status": "updated",
                    "title": updated_task.title
                }
            else:
                return {
                    "status": "error",
                    "error": "Task not found or unauthorized"
                }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to update task: {str(e)}"
            }

    def get_input_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's input"""
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "Who owns the task"
                },
                "task_id": {
                    "type": "integer",
                    "description": "Which task to update"
                },
                "title": {
                    "type": "string",
                    "description": "New task title"
                },
                "description": {
                    "type": "string",
                    "description": "New task description"
                }
            },
            "required": ["user_id", "task_id"],
            "minProperties": 3,
            "maxProperties": 4,
            "additionalProperties": False
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's output"""
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "Echo back the task ID"
                },
                "status": {
                    "type": "string",
                    "enum": ["updated"]
                },
                "title": {
                    "type": "string",
                    "description": "The updated title"
                }
            },
            "required": ["task_id", "status", "title"],
            "additionalProperties": False
        }