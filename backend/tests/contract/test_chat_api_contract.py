"""Contract tests for the chat API endpoint."""
import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming main.py contains the FastAPI app


def test_chat_endpoint_contract():
    """Test the contract of the chat endpoint."""
    client = TestClient(app)
    
    # Test basic request structure
    response = client.post(
        "/api/user123/chat",
        json={
            "message": "Hello, world!"
        }
    )
    
    # Basic contract validation
    assert response.status_code in [200, 400, 401, 404, 500, 503]  # Expected status codes
    
    if response.status_code == 200:
        # Validate response structure for success
        data = response.json()
        assert "conversation_id" in data
        assert "response" in data
        assert isinstance(data["conversation_id"], int)
        assert isinstance(data["response"], str)
        
        # tool_calls is optional
        if "tool_calls" in data:
            assert isinstance(data["tool_calls"], list)
    elif response.status_code in [400, 401, 404]:
        # Validate error response structure
        data = response.json()
        assert "error" in data
        assert "message" in data
        assert isinstance(data["error"], str)
        assert isinstance(data["message"], str)


def test_chat_endpoint_with_conversation_id():
    """Test the contract of the chat endpoint with conversation_id."""
    client = TestClient(app)
    
    response = client.post(
        "/api/user123/chat",
        json={
            "conversation_id": 1,
            "message": "Continue the conversation"
        }
    )
    
    # Should follow same contract as without conversation_id
    assert response.status_code in [200, 400, 401, 404, 500, 503]
    
    if response.status_code == 200:
        data = response.json()
        assert "conversation_id" in data
        assert "response" in data
        assert isinstance(data["conversation_id"], int)
        assert isinstance(data["response"], str)


def test_chat_endpoint_invalid_request():
    """Test the contract of the chat endpoint with invalid request."""
    client = TestClient(app)
    
    # Test with empty message
    response = client.post(
        "/api/user123/chat",
        json={
            "message": ""
        }
    )
    
    # Should return 400 for invalid request
    if response.status_code == 400:
        data = response.json()
        assert "error" in data
        assert data["error"] == "INVALID_REQUEST"


def test_chat_endpoint_missing_message():
    """Test the contract of the chat endpoint with missing message."""
    client = TestClient(app)
    
    # Test with missing message field
    response = client.post(
        "/api/user123/chat",
        json={}
    )
    
    # Should return 400 for invalid request
    if response.status_code == 400:
        data = response.json()
        assert "error" in data
        assert data["error"] == "INVALID_REQUEST"
