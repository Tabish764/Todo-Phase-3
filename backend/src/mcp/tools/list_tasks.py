"""
List Tasks Tool Implementation

This module implements the list_tasks tool for the MCP server.
"""
import json
import logging
from typing import Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.mcp_tool import ListTasksInput, ListTasksOutput, TaskItem, MCPToolBase
from src.services.mcp_service import TaskMCPService
from src.utils.validation import validate_list_tasks_input
from src.utils.auth import verify_user_exists


# Set up logging
logger = logging.getLogger(__name__)


class ListTasksTool(MCPToolBase):
    """Implementation of the list_tasks MCP tool"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the list_tasks tool with given input data"""
        logger.info(f"Executing list_tasks tool for user: {input_data.get('user_id', 'unknown')}")

        # Validate input
        is_valid, error_msg = validate_list_tasks_input(input_data)
        if not is_valid:
            error_response = {
                "status": "error",
                "error": error_msg
            }
            logger.warning(f"Input validation failed for list_tasks: {error_msg}")
            return error_response

        # Extract input values
        user_id = input_data["user_id"]
        status_filter = input_data.get("status", "all")

        # Verify user exists
        user_exists = await verify_user_exists(self.db_session, user_id)
        if not user_exists:
            error_response = {
                "status": "error",
                "error": "User not found"
            }
            logger.warning(f"User not found for list_tasks: {user_id}")
            return error_response

        # Get tasks using the service
        service = TaskMCPService(self.db_session)
        try:
            tasks, total_count = await service.get_user_tasks(user_id, status_filter)

            # Convert tasks to spec format: [{id, title, completed}, ...]
            # Spec says return array directly, not wrapped in object
            task_items = []
            for task in tasks:
                # Convert UUID to integer for spec compliance
                task_id_int = int(str(task.id).replace('-', '')[:12], 16) % (10**9)
                task_items.append({
                    "id": task_id_int,
                    "title": task.title,
                    "completed": task.completed
                })

            # Return array directly as per spec
            logger.info(f"Successfully retrieved {len(tasks)} tasks for user {user_id}")
            return task_items
        except Exception as e:
            error_response = {
                "status": "error",
                "error": f"Failed to retrieve tasks: {str(e)}"
            }
            logger.error(f"Failed to retrieve tasks for user {user_id}: {str(e)}", exc_info=True)
            return error_response

    def get_input_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's input"""
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "Whose tasks to retrieve"
                },
                "status": {
                    "type": "string",
                    "enum": ["all", "pending", "completed"],
                    "default": "all",
                    "description": "Filter by completion status"
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's output"""
        return {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "title": {
                        "type": "string"
                    },
                    "completed": {
                        "type": "boolean"
                    }
                },
                "required": ["id", "title", "completed"],
                "additionalProperties": False
            }
        }