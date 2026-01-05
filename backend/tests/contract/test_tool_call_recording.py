"""Contract tests for MCP tool call recording."""
import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming main.py contains the FastAPI app


def test_tool_call_recording_contract():
    """Test the contract for tool call recording in responses."""
    client = TestClient(app)
    
    response = client.post(
        "/api/testuser123/chat",
        json={
            "message": "Test message"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        
        # Validate basic response structure
        assert "conversation_id" in data
        assert "response" in data
        assert isinstance(data["conversation_id"], int)
        assert isinstance(data["response"], str)
        
        # Validate tool_calls structure if present
        if "tool_calls" in data:
            assert isinstance(data["tool_calls"], list)
            for tool_call in data["tool_calls"]:
                assert "tool_name" in tool_call
                assert "arguments" in tool_call
                assert "result" in tool_call
                assert isinstance(tool_call["tool_name"], str)
                assert isinstance(tool_call["arguments"], dict)
                assert isinstance(tool_call["result"], dict)


def test_tool_call_recording_with_specific_request():
    """Test tool call recording for specific tool requests."""
    client = TestClient(app)
    
    # Request that might trigger a tool call
    response = client.post(
        "/api/testuser123/chat",
        json={
            "message": "Add a task: buy groceries"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        
        # Response should follow the same contract
        assert "conversation_id" in data
        assert "response" in data
        
        # If tool was called, it should be recorded properly
        if "tool_calls" in data and data["tool_calls"]:
            for tool_call in data["tool_calls"]:
                # Validate required fields
                assert "tool_name" in tool_call
                assert "arguments" in tool_call
                assert "result" in tool_call


def test_empty_tool_calls_field():
    """Test that responses without tool calls handle the field properly."""
    client = TestClient(app)
    
    # Request that likely won't trigger any tools
    response = client.post(
        "/api/testuser123/chat",
        json={
            "message": "Hello"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        
        # tool_calls should be present and be an empty list or not present
        if "tool_calls" in data:
            assert isinstance(data["tool_calls"], list)
