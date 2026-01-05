"""
MCP Router Implementation

This module implements the API endpoints for MCP tools.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
from src.database.session import get_db_session
from src.mcp.server import mcp_server
from src.mcp.tools.add_task import AddTaskTool
from src.mcp.tools.list_tasks import ListTasksTool
from src.mcp.tools.complete_task import CompleteTaskTool
from src.mcp.tools.delete_task import DeleteTaskTool
from src.mcp.tools.update_task import UpdateTaskTool
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/mcp", tags=["mcp"])
router._rate_limit_exceeded_handler = _rate_limit_exceeded_handler


@router.get("/tools", response_model=Dict[str, Any])
@limiter.limit("30/minute")
async def get_mcp_tools(request: Request):
    """Get list of all available MCP tools with their schemas"""
    try:
        tools_list = mcp_server.list_all_tools()
        return {"tools": tools_list}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving MCP tools: {str(e)}"
        )


@router.post("/tools/{tool_name}", response_model=Dict[str, Any])
@limiter.limit("20/minute")
async def execute_mcp_tool(
    request: Request,
    tool_name: str,
    input_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session)
):
    """Execute a specific MCP tool"""
    try:
        # Get the tool from the server
        tool = mcp_server.get_tool(tool_name)
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"MCP tool '{tool_name}' not found"
            )

        # Execute the tool
        result = await tool.execute(input_data)
        return result

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing MCP tool '{tool_name}': {str(e)}"
        )


# Initialize tools when the module is loaded
async def initialize_mcp_tools(db_session: AsyncSession):
    """Initialize all MCP tools with the database session"""
    # Register add_task tool
    add_task_tool = AddTaskTool(db_session)
    mcp_server.register_tool("add_task", add_task_tool)

    # Register list_tasks tool
    list_tasks_tool = ListTasksTool(db_session)
    mcp_server.register_tool("list_tasks", list_tasks_tool)

    # Register complete_task tool
    complete_task_tool = CompleteTaskTool(db_session)
    mcp_server.register_tool("complete_task", complete_task_tool)

    # Register delete_task tool
    delete_task_tool = DeleteTaskTool(db_session)
    mcp_server.register_tool("delete_task", delete_task_tool)

    # Register update_task tool
    update_task_tool = UpdateTaskTool(db_session)
    mcp_server.register_tool("update_task", update_task_tool)