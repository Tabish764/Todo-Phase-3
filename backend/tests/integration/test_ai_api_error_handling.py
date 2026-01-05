"""Integration tests for AI API error handling."""
import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming main.py contains the FastAPI app
from unittest.mock import patch, MagicMock


def test_ai_api_connection_error():
    """Test error handling when AI API is unavailable."""
    client = TestClient(app)
    
    # Mock the AI agent service to raise an exception
    with patch('backend.services.ai_agent_service.AIAgentService.process_message') as mock_process:
        mock_process.side_effect = Exception("AI API connection failed")
        
        response = client.post(
            "/api/testuser123/chat",
            json={
                "message": "Test message"
            }
        )
        
        # Should return 500 Internal Server Error or 503 Service Unavailable
        assert response.status_code in [500, 503]
        if response.status_code == 500:
            data = response.json()
            assert "error" in data


def test_ai_api_timeout():
    """Test error handling when AI API request times out."""
    client = TestClient(app)
    
    # Mock the AI agent service to simulate a timeout
    with patch('backend.services.ai_agent_service.AIAgentService.process_message') as mock_process:
        from backend.utils.errors import AIServiceError
        mock_process.side_effect = AIServiceError("AI API request timed out")
        
        response = client.post(
            "/api/testuser123/chat",
            json={
                "message": "Test message that causes timeout"
            }
        )
        
        # Should return 500 Internal Server Error
        assert response.status_code == 500
        data = response.json()
        assert "error" in data
        assert data["error"] == "AI_SERVICE_ERROR"


def test_ai_api_invalid_response():
    """Test error handling when AI API returns invalid response."""
    client = TestClient(app)
    
    # Mock the AI agent service to return an invalid response
    with patch('backend.services.ai_agent_service.AIAgentService.process_message') as mock_process:
        mock_process.side_effect = Exception("Invalid AI response format")
        
        response = client.post(
            "/api/testuser123/chat",
            json={
                "message": "Test message"
            }
        )
        
        # Should return 500 Internal Server Error
        assert response.status_code in [500, 503]


def test_ai_api_quota_exceeded():
    """Test error handling when AI API quota is exceeded."""
    client = TestClient(app)
    
    # Mock the AI agent service to simulate quota exceeded error
    with patch('backend.services.ai_agent_service.AIAgentService.process_message') as mock_process:
        from backend.utils.errors import AIServiceError
        mock_process.side_effect = AIServiceError("AI API quota exceeded")
        
        response = client.post(
            "/api/testuser123/chat",
            json={
                "message": "Test message"
            }
        )
        
        # Should return 500 Internal Server Error
        assert response.status_code == 500
        data = response.json()
        assert "error" in data
        assert data["error"] == "AI_SERVICE_ERROR"
