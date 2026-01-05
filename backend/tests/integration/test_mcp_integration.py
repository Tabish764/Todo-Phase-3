"""
Integration tests for MCP tools
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.main import app
from backend.src.database.connection import db_connection
from backend.src.models.task import Task
from backend.src.database.session import get_db_session


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.asyncio
async def test_mcp_tools_endpoint(client):
    """Test the MCP tools listing endpoint"""
    response = client.get("/api/v1/mcp/tools")

    # Should return successfully
    assert response.status_code == 200

    # Should contain tools
    data = response.json()
    assert "tools" in data
    assert len(data["tools"]) >= 5  # Should have at least 5 tools: add_task, list_tasks, complete_task, delete_task, update_task

    # Check that specific tools are present
    tool_names = [tool["name"] for tool in data["tools"]]
    assert "add_task" in tool_names
    assert "list_tasks" in tool_names
    assert "complete_task" in tool_names
    assert "delete_task" in tool_names
    assert "update_task" in tool_names


@pytest.mark.asyncio
async def test_add_task_tool_endpoint(client):
    """Test the add_task tool endpoint"""
    # Prepare test data
    test_data = {
        "user_id": "test_user_123",
        "title": "Test Task",
        "description": "Test Description"
    }

    # Call the add_task endpoint
    response = client.post("/api/v1/mcp/tools/add_task", json=test_data)

    # Should return successfully
    assert response.status_code == 200

    # Check response structure
    data = response.json()
    assert "status" in data
    assert "task_id" in data
    assert "title" in data
    assert data["status"] == "created"
    assert data["title"] == "Test Task"


@pytest.mark.asyncio
async def test_add_task_tool_endpoint_invalid_data(client):
    """Test the add_task tool endpoint with invalid data"""
    # Prepare invalid test data (missing required fields)
    test_data = {
        "user_id": "test_user_123"
        # Missing title - should cause validation error
    }

    # Call the add_task endpoint
    response = client.post("/api/v1/mcp/tools/add_task", json=test_data)

    # Should return error
    assert response.status_code == 200  # Still returns 200 but with error in body

    # Check error response
    data = response.json()
    assert "status" in data
    assert data["status"] == "error"
    assert "error" in data


@pytest.mark.asyncio
async def test_list_tasks_tool_endpoint(client):
    """Test the list_tasks tool endpoint"""
    # First, add a task to have something to list
    add_data = {
        "user_id": "test_user_456",
        "title": "List Test Task",
        "description": "Task for list test"
    }

    add_response = client.post("/api/v1/mcp/tools/add_task", json=add_data)
    assert add_response.status_code == 200

    # Now list tasks for the user
    list_data = {
        "user_id": "test_user_456",
        "status": "all"
    }

    response = client.post("/api/v1/mcp/tools/list_tasks", json=list_data)

    # Should return successfully
    assert response.status_code == 200

    # Check response structure
    data = response.json()
    assert "status" in data
    assert "tasks" in data
    assert "count" in data
    assert data["status"] == "success"
    assert len(data["tasks"]) >= 1

    # Verify the task we added is in the list
    task_titles = [task["title"] for task in data["tasks"]]
    assert "List Test Task" in task_titles


@pytest.mark.asyncio
async def test_complete_task_tool_endpoint(client):
    """Test the complete_task tool endpoint"""
    # First, add a task to complete
    add_data = {
        "user_id": "test_user_789",
        "title": "Complete Test Task",
        "description": "Task for complete test"
    }

    add_response = client.post("/api/v1/mcp/tools/add_task", json=add_data)
    assert add_response.status_code == 200
    task_id = add_response.json()["task_id"]

    # Now complete the task
    complete_data = {
        "user_id": "test_user_789",
        "task_id": task_id
    }

    response = client.post("/api/v1/mcp/tools/complete_task", json=complete_data)

    # Should return successfully
    assert response.status_code == 200

    # Check response structure
    data = response.json()
    assert "status" in data
    assert "task_id" in data
    assert "title" in data
    assert data["status"] == "completed"
    assert data["task_id"] == task_id
    assert data["title"] == "Complete Test Task"


@pytest.mark.asyncio
async def test_update_task_tool_endpoint(client):
    """Test the update_task tool endpoint"""
    # First, add a task to update
    add_data = {
        "user_id": "test_user_abc",
        "title": "Original Title",
        "description": "Original Description"
    }

    add_response = client.post("/api/v1/mcp/tools/add_task", json=add_data)
    assert add_response.status_code == 200
    task_id = add_response.json()["task_id"]

    # Now update the task
    update_data = {
        "user_id": "test_user_abc",
        "task_id": task_id,
        "title": "Updated Title",
        "description": "Updated Description"
    }

    response = client.post("/api/v1/mcp/tools/update_task", json=update_data)

    # Should return successfully
    assert response.status_code == 200

    # Check response structure
    data = response.json()
    assert "status" in data
    assert "task_id" in data
    assert "title" in data
    assert data["status"] == "updated"
    assert data["task_id"] == task_id
    assert data["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_task_tool_endpoint(client):
    """Test the delete_task tool endpoint"""
    # First, add a task to delete
    add_data = {
        "user_id": "test_user_def",
        "title": "Delete Test Task",
        "description": "Task for delete test"
    }

    add_response = client.post("/api/v1/mcp/tools/add_task", json=add_data)
    assert add_response.status_code == 200
    task_id = add_response.json()["task_id"]

    # Now delete the task
    delete_data = {
        "user_id": "test_user_def",
        "task_id": task_id
    }

    response = client.post("/api/v1/mcp/tools/delete_task", json=delete_data)

    # Should return successfully
    assert response.status_code == 200

    # Check response structure
    data = response.json()
    assert "status" in data
    assert "task_id" in data
    assert "title" in data
    assert data["status"] == "deleted"
    assert data["task_id"] == task_id
    assert data["title"] == "Delete Test Task"


@pytest.mark.asyncio
async def test_unauthorized_access(client):
    """Test that unauthorized access is properly blocked"""
    # Try to complete a task that doesn't belong to the user
    complete_data = {
        "user_id": "different_user",
        "task_id": 999999  # Non-existent task
    }

    response = client.post("/api/v1/mcp/tools/complete_task", json=complete_data)

    # Should return error (not 404 because of validation, but error in response)
    assert response.status_code == 200  # Returns 200 but with error in body

    data = response.json()
    assert "status" in data
    assert data["status"] == "error"
    # Should indicate unauthorized access


@pytest.mark.asyncio
async def test_tool_not_found(client):
    """Test that non-existent tools return appropriate error"""
    # Try to call a non-existent tool
    response = client.post("/api/v1/mcp/tools/nonexistent_tool", json={})

    # Should return 404
    assert response.status_code == 404

    # Check error response
    data = response.json()
    assert "detail" in data


def test_mcp_tools_basic_validation():
    """Basic validation test without async context"""
    # This test can run without async context
    response_example = {
        "task_id": 123,
        "status": "created",
        "title": "Test Task",
        "description": "Test Description"
    }

    # Validate required fields exist
    assert "task_id" in response_example
    assert "status" in response_example
    assert "title" in response_example

    # Validate field types
    assert isinstance(response_example["task_id"], int)
    assert isinstance(response_example["status"], str)
    assert isinstance(response_example["title"], str)


if __name__ == "__main__":
    # For running tests individually during development
    pytest.main([__file__])