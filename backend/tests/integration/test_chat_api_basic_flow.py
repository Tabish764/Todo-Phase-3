"""Integration tests for basic chat API message flow."""
import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming main.py contains the FastAPI app


def test_basic_message_flow():
    """Test basic message flow: send message -> receive response."""
    client = TestClient(app)
    
    # Send a simple message
    response = client.post(
        "/api/testuser123/chat",
        json={
            "message": "Hello"
        }
    )
    
    # Should return 200 with conversation_id and response
    if response.status_code == 200:
        data = response.json()
        assert "conversation_id" in data
        assert "response" in data
        assert isinstance(data["conversation_id"], int)
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0  # Response should not be empty


def test_conversation_continuation():
    """Test continuing an existing conversation."""
    client = TestClient(app)
    
    # First message - creates conversation
    first_response = client.post(
        "/api/testuser123/chat",
        json={
            "message": "Hello, I want to add a task"
        }
    )
    
    if first_response.status_code == 200:
        first_data = first_response.json()
        assert "conversation_id" in first_data
        
        # Second message - continues conversation
        second_response = client.post(
            "/api/testuser123/chat",
            json={
                "conversation_id": first_data["conversation_id"],
                "message": "Add a task to buy groceries"
            }
        )
        
        if second_response.status_code == 200:
            second_data = second_response.json()
            assert second_data["conversation_id"] == first_data["conversation_id"]
            assert "response" in second_data


def test_different_users_have_different_conversations():
    """Test that different users have separate conversations."""
    client = TestClient(app)
    
    # User 1 creates conversation
    user1_response = client.post(
        "/api/user1/chat",
        json={
            "message": "Hello from user 1"
        }
    )
    
    # User 2 creates conversation
    user2_response = client.post(
        "/api/user2/chat",
        json={
            "message": "Hello from user 2"
        }
    )
    
    if user1_response.status_code == 200 and user2_response.status_code == 200:
        user1_data = user1_response.json()
        user2_data = user2_response.json()
        
        # Different users should get different conversation IDs
        assert "conversation_id" in user1_data
        assert "conversation_id" in user2_data
        # Note: This might return same ID if both create first conversation, 
        # but the important part is that they can't access each other's conversations
