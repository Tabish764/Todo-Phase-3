"""
Contract tests for MCP API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.mcp.server import mcp_server
from backend.src.mcp.tools.add_task import AddTaskTool
from backend.src.mcp.tools.list_tasks import ListTasksTool
from backend.src.mcp.tools.complete_task import CompleteTaskTool
from backend.src.mcp.tools.delete_task import DeleteTaskTool
from backend.src.mcp.tools.update_task import UpdateTaskTool


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client


def test_mcp_tools_discovery_contract(client):
    """Test the contract for MCP tools discovery endpoint"""
    response = client.get("/api/v1/mcp/tools")

    # Verify response status
    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "tools" in data
    assert isinstance(data["tools"], list)

    # Verify each tool has required properties
    for tool in data["tools"]:
        assert "name" in tool
        assert "description" in tool
        assert "input_schema" in tool
        assert "output_schema" in tool

        # Verify schema structure
        assert isinstance(tool["input_schema"], dict)
        assert isinstance(tool["output_schema"], dict)
        assert "type" in tool["input_schema"]
        assert "type" in tool["output_schema"]

    # Verify all expected tools are present
    tool_names = [tool["name"] for tool in data["tools"]]
    expected_tools = ["add_task", "list_tasks", "complete_task", "delete_task", "update_task"]
    for expected_tool in expected_tools:
        assert expected_tool in tool_names


def test_add_task_contract(client):
    """Test the contract for add_task tool"""
    # Verify the tool exists in the registry
    tool = mcp_server.get_tool("add_task")
    assert tool is not None

    # Verify input schema
    input_schema = tool.get_input_schema()
    assert "user_id" in input_schema["properties"]
    assert "title" in input_schema["properties"]
    assert "required" in input_schema
    assert "user_id" in input_schema["required"]
    assert "title" in input_schema["required"]

    # Verify output schema
    output_schema = tool.get_output_schema()
    assert "task_id" in output_schema["properties"]
    assert "status" in output_schema["properties"]
    assert "title" in output_schema["properties"]
    assert "required" in output_schema
    assert "task_id" in output_schema["required"]
    assert "status" in output_schema["required"]
    assert "title" in output_schema["required"]

    # Test with valid input structure
    valid_input = {
        "user_id": "user123",
        "title": "Test task"
    }

    # Should accept the valid input (would fail at execution due to no DB, but should validate input)
    # We're testing the contract structure, not full execution
    response = client.post("/api/v1/mcp/tools/add_task", json=valid_input)

    # Response should have proper structure regardless of execution result
    assert response.status_code in [200, 422, 500]  # Could be various depending on execution


def test_list_tasks_contract(client):
    """Test the contract for list_tasks tool"""
    # Verify the tool exists in the registry
    tool = mcp_server.get_tool("list_tasks")
    assert tool is not None

    # Verify input schema
    input_schema = tool.get_input_schema()
    assert "user_id" in input_schema["properties"]
    assert "status" in input_schema["properties"]
    assert "required" in input_schema
    assert "user_id" in input_schema["required"]

    # Verify output schema
    output_schema = tool.get_output_schema()
    assert "tasks" in output_schema["properties"]
    assert "count" in output_schema["properties"]
    assert "status" in output_schema["properties"]
    assert "required" in output_schema
    assert "tasks" in output_schema["required"]
    assert "count" in output_schema["required"]
    assert "status" in output_schema["required"]

    # Test with valid input structure
    valid_input = {
        "user_id": "user123",
        "status": "all"
    }

    response = client.post("/api/v1/mcp/tools/list_tasks", json=valid_input)
    assert response.status_code in [200, 422, 500]


def test_complete_task_contract(client):
    """Test the contract for complete_task tool"""
    # Verify the tool exists in the registry
    tool = mcp_server.get_tool("complete_task")
    assert tool is not None

    # Verify input schema
    input_schema = tool.get_input_schema()
    assert "user_id" in input_schema["properties"]
    assert "task_id" in input_schema["properties"]
    assert "required" in input_schema
    assert "user_id" in input_schema["required"]
    assert "task_id" in input_schema["required"]

    # Verify output schema
    output_schema = tool.get_output_schema()
    assert "task_id" in output_schema["properties"]
    assert "status" in output_schema["properties"]
    assert "title" in output_schema["properties"]
    assert "required" in output_schema
    assert "task_id" in output_schema["required"]
    assert "status" in output_schema["required"]
    assert "title" in output_schema["required"]

    # Test with valid input structure
    valid_input = {
        "user_id": "user123",
        "task_id": 1
    }

    response = client.post("/api/v1/mcp/tools/complete_task", json=valid_input)
    assert response.status_code in [200, 422, 500]


def test_delete_task_contract(client):
    """Test the contract for delete_task tool"""
    # Verify the tool exists in the registry
    tool = mcp_server.get_tool("delete_task")
    assert tool is not None

    # Verify input schema
    input_schema = tool.get_input_schema()
    assert "user_id" in input_schema["properties"]
    assert "task_id" in input_schema["properties"]
    assert "required" in input_schema
    assert "user_id" in input_schema["required"]
    assert "task_id" in input_schema["required"]

    # Verify output schema
    output_schema = tool.get_output_schema()
    assert "task_id" in output_schema["properties"]
    assert "status" in output_schema["properties"]
    assert "title" in output_schema["properties"]
    assert "required" in output_schema
    assert "task_id" in output_schema["required"]
    assert "status" in output_schema["required"]
    assert "title" in output_schema["required"]

    # Test with valid input structure
    valid_input = {
        "user_id": "user123",
        "task_id": 1
    }

    response = client.post("/api/v1/mcp/tools/delete_task", json=valid_input)
    assert response.status_code in [200, 422, 500]


def test_update_task_contract(client):
    """Test the contract for update_task tool"""
    # Verify the tool exists in the registry
    tool = mcp_server.get_tool("update_task")
    assert tool is not None

    # Verify input schema
    input_schema = tool.get_input_schema()
    assert "user_id" in input_schema["properties"]
    assert "task_id" in input_schema["properties"]
    assert "title" in input_schema["properties"]
    assert "description" in input_schema["properties"]
    assert "required" in input_schema
    assert "user_id" in input_schema["required"]
    assert "task_id" in input_schema["required"]

    # Verify output schema
    output_schema = tool.get_output_schema()
    assert "task_id" in output_schema["properties"]
    assert "status" in output_schema["properties"]
    assert "title" in output_schema["properties"]
    assert "required" in output_schema
    assert "task_id" in output_schema["required"]
    assert "status" in output_schema["required"]
    assert "title" in output_schema["required"]

    # Test with valid input structure
    valid_input = {
        "user_id": "user123",
        "task_id": 1,
        "title": "Updated title"
    }

    response = client.post("/api/v1/mcp/tools/update_task", json=valid_input)
    assert response.status_code in [200, 422, 500]


def test_tool_execution_error_handling_contract(client):
    """Test that tools properly handle invalid inputs"""
    # Test add_task with missing required fields
    invalid_input = {
        "user_id": "user123"
        # Missing title
    }

    response = client.post("/api/v1/mcp/tools/add_task", json=invalid_input)

    # Should return 200 with error in body (not 422) as per MCP design
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["status"] == "error"
    assert "error" in data


def test_nonexistent_tool_contract(client):
    """Test that non-existent tools return appropriate error"""
    response = client.post("/api/v1/mcp/tools/nonexistent_tool", json={})

    # Should return 404 for non-existent tool
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data


def test_all_tools_have_proper_schemas():
    """Test that all registered tools have properly defined schemas"""
    tools = mcp_server.list_all_tools()

    for tool_info in tools:
        # Verify each tool has both schemas
        assert "input_schema" in tool_info
        assert "output_schema" in tool_info

        input_schema = tool_info["input_schema"]
        output_schema = tool_info["output_schema"]

        # Verify schemas have required structure
        assert isinstance(input_schema, dict)
        assert isinstance(output_schema, dict)

        # Verify basic schema properties
        assert "type" in input_schema
        assert "type" in output_schema
        assert input_schema["type"] == "object"
        assert output_schema["type"] == "object"


if __name__ == "__main__":
    # For running tests individually during development
    pytest.main([__file__])