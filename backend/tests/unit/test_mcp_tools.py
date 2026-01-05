"""
Unit tests for MCP tools
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.mcp.tools.add_task import AddTaskTool
from backend.src.mcp.tools.list_tasks import ListTasksTool
from backend.src.mcp.tools.complete_task import CompleteTaskTool
from backend.src.mcp.tools.delete_task import DeleteTaskTool
from backend.src.mcp.tools.update_task import UpdateTaskTool
from backend.src.models.task import Task


@pytest.mark.asyncio
async def test_add_task_tool_execute_success():
    """Test successful execution of add_task tool"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = AddTaskTool(mock_db_session)

    # Mock input data
    input_data = {
        "user_id": "user123",
        "title": "Test task",
        "description": "Test description"
    }

    # Mock task creation
    mock_task = Task(
        id=1,
        user_id="user123",
        title="Test task",
        description="Test description",
        completed=False
    )

    # Mock the service to return the created task
    import backend.src.services.mcp_service as mcp_service_module
    original_create_task = mcp_service_module.TaskMCPService.create_task

    async def mock_create_task(self, user_id, title, description):
        return mock_task

    # Patch the service method
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr("backend.src.services.mcp_service.TaskMCPService.create_task", mock_create_task)

        # Execute the tool
        result = await tool.execute(input_data)

        # Verify the result
        assert result["status"] == "created"
        assert result["task_id"] == 1
        assert result["title"] == "Test task"
        assert result["description"] == "Test description"


@pytest.mark.asyncio
async def test_add_task_tool_execute_missing_user_id():
    """Test add_task tool with missing user_id"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = AddTaskTool(mock_db_session)

    # Mock input data without user_id
    input_data = {
        "title": "Test task"
    }

    # Execute the tool
    result = await tool.execute(input_data)

    # Verify the error response
    assert result["status"] == "error"
    assert "User ID is required" in result["error"]


@pytest.mark.asyncio
async def test_add_task_tool_execute_missing_title():
    """Test add_task tool with missing title"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = AddTaskTool(mock_db_session)

    # Mock input data without title
    input_data = {
        "user_id": "user123"
    }

    # Execute the tool
    result = await tool.execute(input_data)

    # Verify the error response
    assert result["status"] == "error"
    assert "Task title is required" in result["error"]


@pytest.mark.asyncio
async def test_list_tasks_tool_execute_success():
    """Test successful execution of list_tasks tool"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = ListTasksTool(mock_db_session)

    # Mock input data
    input_data = {
        "user_id": "user123",
        "status": "all"
    }

    # Mock tasks
    mock_task = Task(
        id=1,
        user_id="user123",
        title="Test task",
        description="Test description",
        completed=False
    )

    # Mock the service to return tasks
    import backend.src.services.mcp_service as mcp_service_module
    original_get_user_tasks = mcp_service_module.TaskMCPService.get_user_tasks

    async def mock_get_user_tasks(self, user_id, status_filter, limit=100, offset=0):
        return [mock_task], 1

    # Patch the service method
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr("backend.src.services.mcp_service.TaskMCPService.get_user_tasks", mock_get_user_tasks)

        # Execute the tool
        result = await tool.execute(input_data)

        # Verify the result
        assert result["status"] == "success"
        assert result["count"] == 1
        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["title"] == "Test task"


@pytest.mark.asyncio
async def test_complete_task_tool_execute_success():
    """Test successful execution of complete_task tool"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = CompleteTaskTool(mock_db_session)

    # Mock input data
    input_data = {
        "user_id": "user123",
        "task_id": 1
    }

    # Mock task
    mock_task = Task(
        id=1,
        user_id="user123",
        title="Test task",
        description="Test description",
        completed=False
    )

    # Mock the service to return updated task
    import backend.src.services.mcp_service as mcp_service_module
    original_update_task_completion = mcp_service_module.TaskMCPService.update_task_completion

    async def mock_update_task_completion(self, task_id, user_id, completed):
        mock_task.completed = completed
        return mock_task

    # Patch the service method
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr("backend.src.services.mcp_service.TaskMCPService.update_task_completion", mock_update_task_completion)

        # Execute the tool
        result = await tool.execute(input_data)

        # Verify the result
        assert result["status"] == "completed"
        assert result["task_id"] == 1
        assert result["title"] == "Test task"


@pytest.mark.asyncio
async def test_delete_task_tool_execute_success():
    """Test successful execution of delete_task tool"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = DeleteTaskTool(mock_db_session)

    # Mock input data
    input_data = {
        "user_id": "user123",
        "task_id": 1
    }

    # Mock task
    mock_task = Task(
        id=1,
        user_id="user123",
        title="Test task",
        description="Test description",
        completed=False
    )

    # Mock the service to return True for successful deletion
    import backend.src.services.mcp_service as mcp_service_module
    original_delete_task = mcp_service_module.TaskMCPService.delete_task
    original_get_task_by_id = mcp_service_module.TaskMCPService.get_task_by_id

    async def mock_delete_task(self, task_id, user_id):
        return True

    async def mock_get_task_by_id(self, task_id, user_id):
        return mock_task

    # Patch the service methods
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr("backend.src.services.mcp_service.TaskMCPService.delete_task", mock_delete_task)
        mp.setattr("backend.src.services.mcp_service.TaskMCPService.get_task_by_id", mock_get_task_by_id)

        # Execute the tool
        result = await tool.execute(input_data)

        # Verify the result
        assert result["status"] == "deleted"
        assert result["task_id"] == 1
        assert result["title"] == "Test task"


@pytest.mark.asyncio
async def test_update_task_tool_execute_success():
    """Test successful execution of update_task tool"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = UpdateTaskTool(mock_db_session)

    # Mock input data
    input_data = {
        "user_id": "user123",
        "task_id": 1,
        "title": "Updated title"
    }

    # Mock task
    mock_task = Task(
        id=1,
        user_id="user123",
        title="Updated title",
        description="Test description",
        completed=False
    )

    # Mock the service to return updated task
    import backend.src.services.mcp_service as mcp_service_module
    original_update_task_details = mcp_service_module.TaskMCPService.update_task_details

    async def mock_update_task_details(self, task_id, user_id, title=None, description=None):
        if title:
            mock_task.title = title
        if description is not None:
            mock_task.description = description
        return mock_task

    # Patch the service method
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr("backend.src.services.mcp_service.TaskMCPService.update_task_details", mock_update_task_details)

        # Execute the tool
        result = await tool.execute(input_data)

        # Verify the result
        assert result["status"] == "updated"
        assert result["task_id"] == 1
        assert result["title"] == "Updated title"


def test_add_task_tool_schemas():
    """Test that add_task tool returns correct schemas"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = AddTaskTool(mock_db_session)

    # Test input schema
    input_schema = tool.get_input_schema()
    assert "user_id" in input_schema["properties"]
    assert "title" in input_schema["properties"]
    assert "description" in input_schema["properties"]
    assert "user_id" in input_schema["required"]
    assert "title" in input_schema["required"]

    # Test output schema
    output_schema = tool.get_output_schema()
    assert "task_id" in output_schema["properties"]
    assert "status" in output_schema["properties"]
    assert "title" in output_schema["properties"]
    assert "task_id" in output_schema["required"]
    assert "status" in output_schema["required"]
    assert "title" in output_schema["required"]


def test_list_tasks_tool_schemas():
    """Test that list_tasks tool returns correct schemas"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = ListTasksTool(mock_db_session)

    # Test input schema
    input_schema = tool.get_input_schema()
    assert "user_id" in input_schema["properties"]
    assert "status" in input_schema["properties"]
    assert "user_id" in input_schema["required"]

    # Test output schema
    output_schema = tool.get_output_schema()
    assert "tasks" in output_schema["properties"]
    assert "count" in output_schema["properties"]
    assert "status" in output_schema["properties"]
    assert "tasks" in output_schema["required"]
    assert "count" in output_schema["required"]
    assert "status" in output_schema["required"]


def test_complete_task_tool_schemas():
    """Test that complete_task tool returns correct schemas"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = CompleteTaskTool(mock_db_session)

    # Test input schema
    input_schema = tool.get_input_schema()
    assert "user_id" in input_schema["properties"]
    assert "task_id" in input_schema["properties"]
    assert "user_id" in input_schema["required"]
    assert "task_id" in input_schema["required"]

    # Test output schema
    output_schema = tool.get_output_schema()
    assert "task_id" in output_schema["properties"]
    assert "status" in output_schema["properties"]
    assert "title" in output_schema["properties"]
    assert "task_id" in output_schema["required"]
    assert "status" in output_schema["required"]
    assert "title" in output_schema["required"]


def test_delete_task_tool_schemas():
    """Test that delete_task tool returns correct schemas"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = DeleteTaskTool(mock_db_session)

    # Test input schema
    input_schema = tool.get_input_schema()
    assert "user_id" in input_schema["properties"]
    assert "task_id" in input_schema["properties"]
    assert "user_id" in input_schema["required"]
    assert "task_id" in input_schema["required"]

    # Test output schema
    output_schema = tool.get_output_schema()
    assert "task_id" in output_schema["properties"]
    assert "status" in output_schema["properties"]
    assert "title" in output_schema["properties"]
    assert "task_id" in output_schema["required"]
    assert "status" in output_schema["required"]
    assert "title" in output_schema["required"]


def test_update_task_tool_schemas():
    """Test that update_task tool returns correct schemas"""
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Create the tool
    tool = UpdateTaskTool(mock_db_session)

    # Test input schema
    input_schema = tool.get_input_schema()
    assert "user_id" in input_schema["properties"]
    assert "task_id" in input_schema["properties"]
    assert "title" in input_schema["properties"]
    assert "description" in input_schema["properties"]
    assert "user_id" in input_schema["required"]
    assert "task_id" in input_schema["required"]

    # Test output schema
    output_schema = tool.get_output_schema()
    assert "task_id" in output_schema["properties"]
    assert "status" in output_schema["properties"]
    assert "title" in output_schema["properties"]
    assert "description" in output_schema["properties"]
    assert "task_id" in output_schema["required"]
    assert "status" in output_schema["required"]
    assert "title" in output_schema["required"]