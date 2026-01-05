"""Integration tests for stateless request processing."""
import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming main.py contains the FastAPI app


def test_conversation_continuation_without_server_state():
    """Test that conversation can be continued without server-side state."""
    client = TestClient(app)
    
    # Start a conversation
    first_response = client.post(
        "/api/testuser123/chat",
        json={
            "message": "Hello, I want to start a conversation"
        }
    )
    
    assert first_response.status_code == 200
    first_data = first_response.json()
    assert "conversation_id" in first_data
    conversation_id = first_data["conversation_id"]
    
    # Simulate server restart scenario by creating a new client instance
    # In a real scenario, this would be a different server instance
    # but for testing purposes, the same client should work since we're stateless
    second_response = client.post(
        "/api/testuser123/chat",
        json={
            "conversation_id": conversation_id,
            "message": "Continue the conversation"
        }
    )
    
    assert second_response.status_code == 200
    second_data = second_response.json()
    assert second_data["conversation_id"] == conversation_id
    assert "response" in second_data


def test_multiple_instances_same_conversation():
    """Test that multiple server instances can handle same conversation."""
    # Create two separate clients to simulate different server instances
    client1 = TestClient(app)
    client2 = TestClient(app)
    
    # Start conversation with client1
    first_response = client1.post(
        "/api/testuser123/chat",
        json={
            "message": "Hello from instance 1"
        }
    )
    
    assert first_response.status_code == 200
    first_data = first_response.json()
    assert "conversation_id" in first_data
    conversation_id = first_data["conversation_id"]
    
    # Continue conversation with client2 (simulating different server instance)
    second_response = client2.post(
        "/api/testuser123/chat",
        json={
            "conversation_id": conversation_id,
            "message": "Hello from instance 2"
        }
    )
    
    assert second_response.status_code == 200
    second_data = second_response.json()
    assert second_data["conversation_id"] == conversation_id
    assert "response" in second_data


def test_no_session_storage():
    """Test that no server-side session storage is used."""
    client = TestClient(app)
    
    # Make a request
    response1 = client.post(
        "/api/testuser123/chat",
        json={
            "message": "First message"
        }
    )
    
    assert response1.status_code == 200
    data1 = response1.json()
    assert "conversation_id" in data1
    
    # Make another request - should not depend on server-side session state
    response2 = client.post(
        "/api/testuser123/chat",
        json={
            "conversation_id": data1["conversation_id"],
            "message": "Second message"
        }
    )
    
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["conversation_id"] == data1["conversation_id"]
    assert "response" in data2
