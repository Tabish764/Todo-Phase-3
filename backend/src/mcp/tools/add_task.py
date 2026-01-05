"""
Add Task Tool Implementation

This module implements the add_task tool for the MCP server.
"""
import json
import logging
from typing import Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.mcp_tool import AddTaskInput, AddTaskOutput, MCPToolBase
from src.services.mcp_service import TaskMCPService
from src.utils.validation import validate_add_task_input
from src.utils.auth import verify_user_exists


# Set up logging
logger = logging.getLogger(__name__)


class AddTaskTool(MCPToolBase):
    """Implementation of the add_task MCP tool"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the add_task tool with given input data"""
        logger.info(f"Executing add_task tool for user: {input_data.get('user_id', 'unknown')}")

        # Validate input
        is_valid, error_msg = validate_add_task_input(input_data)
        if not is_valid:
            error_response = {
                "status": "error",
                "error": error_msg
            }
            logger.warning(f"Input validation failed for add_task: {error_msg}")
            return error_response

        # Extract input values
        user_id = input_data["user_id"]
        title = input_data["title"]
        description = input_data.get("description")

        # Verify user exists
        user_exists = await verify_user_exists(self.db_session, user_id)
        if not user_exists:
            error_response = {
                "status": "error",
                "error": "User not found"
            }
            logger.warning(f"User not found for add_task: {user_id}")
            return error_response

        # Create task using the service
        service = TaskMCPService(self.db_session)
        try:
            task = await service.create_task(user_id, title, description)

            # Convert UUID to integer for spec compliance (use first 12 hex chars as integer)
            task_id_int = int(str(task.id).replace('-', '')[:12], 16) % (10**9)

            # Return success response matching spec: {task_id, status, title}
            result = {
                "task_id": task_id_int,
                "status": "created",
                "title": task.title
            }
            logger.info(f"Successfully created task {task.id} (ID: {task_id_int}) for user {user_id}")
            return result
        except Exception as e:
            error_response = {
                "status": "error",
                "error": f"Failed to create task: {str(e)}"
            }
            logger.error(f"Failed to create task for user {user_id}: {str(e)}", exc_info=True)
            return error_response

    def get_input_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's input"""
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "Who owns this task"
                },
                "title": {
                    "type": "string",
                    "description": "Task title"
                },
                "description": {
                    "type": "string",
                    "description": "Additional task details",
                    "nullable": True
                }
            },
            "required": ["user_id", "title"],
            "additionalProperties": False
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's output"""
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "ID of created task"
                },
                "status": {
                    "type": "string",
                    "enum": ["created"]
                },
                "title": {
                    "type": "string",
                    "description": "Echo back the title"
                }
            },
            "required": ["task_id", "status", "title"],
            "additionalProperties": False
        }