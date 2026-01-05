"""Integration tests for invalid conversation ID handling."""
import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming main.py contains the FastAPI app


def test_invalid_conversation_id():
    """Test handling of invalid conversation ID."""
    client = TestClient(app)
    
    # Try to access a conversation with an invalid ID
    response = client.post(
        "/api/testuser123/chat",
        json={
            "conversation_id": -1,  # Invalid conversation ID
            "message": "Test message"
        }
    )
    
    # Should return 400 Bad Request for invalid ID format
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"] == "INVALID_REQUEST"


def test_nonexistent_conversation_id():
    """Test handling of non-existent conversation ID."""
    client = TestClient(app)
    
    # Try to access a conversation that doesn't exist
    response = client.post(
        "/api/testuser123/chat",
        json={
            "conversation_id": 999999,  # Non-existent conversation ID
            "message": "Test message"
        }
    )
    
    # Should return 404 Not Found
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"] == "NOT_FOUND"


def test_conversation_access_by_wrong_user():
    """Test that users can't access conversations belonging to other users."""
    client = TestClient(app)
    
    # First, create a conversation with one user
    first_response = client.post(
        "/api/realuser123/chat",
        json={
            "message": "My message"
        }
    )
    
    if first_response.status_code == 200:
        data = first_response.json()
        if "conversation_id" in data:
            conversation_id = data["conversation_id"]
            
            # Try to access the same conversation with a different user
            second_response = client.post(
                "/api/otheruser456/chat",  # Different user
                json={
                    "conversation_id": conversation_id,
                    "message": "Trying to access other's conversation"
                }
            )
            
            # Should return 404 or 403 (Forbidden) since user doesn't own the conversation
            assert second_response.status_code in [403, 404]
