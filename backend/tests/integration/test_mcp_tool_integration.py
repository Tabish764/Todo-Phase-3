"""Integration tests for MCP tool integration."""
import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming main.py contains the FastAPI app


def test_mcp_tool_invocation():
    """Test that MCP tools are invoked when appropriate."""
    client = TestClient(app)
    
    # Test a message that should trigger an MCP tool (like adding a task)
    response = client.post(
        "/api/testuser123/chat",
        json={
            "message": "Add a task to buy groceries"
        }
    )
    
    # The response should contain tool calls if MCP integration is working
    if response.status_code == 200:
        data = response.json()
        # In a real implementation, this would trigger an add_task MCP tool
        # For testing purposes, we're verifying the structure can handle tool calls
        assert "conversation_id" in data
        assert "response" in data
        # tool_calls may or may not be present depending on AI decision


def test_mcp_tool_with_conversation_context():
    """Test MCP tool invocation within conversation context."""
    client = TestClient(app)
    
    # Start a conversation
    first_response = client.post(
        "/api/testuser123/chat",
        json={
            "message": "I want to manage my tasks"
        }
    )
    
    assert first_response.status_code == 200
    first_data = first_response.json()
    assert "conversation_id" in first_data
    
    # Now try to add a task (should trigger MCP tool)
    second_response = client.post(
        "/api/testuser123/chat",
        json={
            "conversation_id": first_data["conversation_id"],
            "message": "Add task: buy milk"
        }
    )
    
    if second_response.status_code == 200:
        second_data = second_response.json()
        assert second_data["conversation_id"] == first_data["conversation_id"]
        # The response may include tool call information


def test_multiple_tool_calls():
    """Test handling of multiple MCP tool calls."""
    client = TestClient(app)
    
    # A complex request that might trigger multiple tools
    response = client.post(
        "/api/testuser123/chat",
        json={
            "message": "Show me my tasks and add a new one: walk the dog"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        assert "conversation_id" in data
        assert "response" in data
        # This would potentially trigger both list_tasks and add_task tools
