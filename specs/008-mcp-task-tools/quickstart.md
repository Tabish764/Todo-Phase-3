# Quickstart: MCP Server with Task Management Tools

## Overview
This guide helps you set up the MCP server with 5 standardized tools for AI agents to interact with the task management system.

## Prerequisites
- Python 3.12
- PostgreSQL database
- FastAPI application
- Existing task management system with user authentication

## Setup Steps

### 1. Install Dependencies
```bash
pip install fastapi pydantic pydantic-settings python-multipart sqlmodel asyncpg alembic psycopg2-binary
```

### 2. Verify Database Connection
Ensure the existing task database is accessible and properly configured.

### 3. Test the MCP Tools
Run the unit tests to ensure the MCP tools work correctly:

```bash
pytest tests/unit/test_mcp_tools.py
```

### 4. Test the MCP Integration
Test the MCP server integration:

```bash
# Test tool discovery
curl -X GET http://localhost:8000/mcp/tools

# Test add_task
curl -X POST http://localhost:8000/mcp/tools/add_task -H "Content-Type: application/json" -d '{"user_id": "user123", "title": "Test task", "description": "Test description"}'

# Test list_tasks
curl -X POST http://localhost:8000/mcp/tools/list_tasks -H "Content-Type: application/json" -d '{"user_id": "user123", "status": "all"}'

# Test complete_task
curl -X POST http://localhost:8000/mcp/tools/complete_task -H "Content-Type: application/json" -d '{"user_id": "user123", "task_id": 1}'

# Test delete_task
curl -X POST http://localhost:8000/mcp/tools/delete_task -H "Content-Type: application/json" -d '{"user_id": "user123", "task_id": 1}'

# Test update_task
curl -X POST http://localhost:8000/mcp/tools/update_task -H "Content-Type: application/json" -d '{"user_id": "user123", "task_id": 1, "title": "Updated title"}'
```

## Key Components

### Models
- `Task`: Represents a user's task with ID, title, description, completion status, and timestamps
- MCP Input/Output models for each tool (add_task, list_tasks, complete_task, delete_task, update_task)

### Services
- `TaskService`: Handles business logic for task operations
- `MCPService`: Handles MCP server operations and tool execution

### API Endpoints
- `GET /mcp/tools`: Get list of available MCP tools with schemas
- `POST /mcp/tools/{tool_name}`: Execute specific MCP tool

## Common Operations

### Using add_task Tool
```python
from backend.src.mcp.tools.add_task import AddTaskTool

tool = AddTaskTool()
result = tool.execute({
    "user_id": "user123",
    "title": "New task",
    "description": "Task description"
})
```

### Using list_tasks Tool
```python
from backend.src.mcp.tools.list_tasks import ListTasksTool

tool = ListTasksTool()
result = tool.execute({
    "user_id": "user123",
    "status": "pending"
})
```

### Using complete_task Tool
```python
from backend.src.mcp.tools.complete_task import CompleteTaskTool

tool = CompleteTaskTool()
result = tool.execute({
    "user_id": "user123",
    "task_id": 1
})
```

## Troubleshooting

### Tool Discovery Issues
If tools are not showing up:
1. Check that MCP server is properly initialized
2. Verify that all 5 tools are registered
3. Run `pytest tests/unit/test_mcp_tools.py` to test discovery

### Authorization Issues
If operations return "Unauthorized" errors:
1. Verify that user_id matches task ownership
2. Check that the authorization logic is properly implemented
3. Ensure the user exists in the system