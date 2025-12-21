import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# To import the app, we need to add the project root to the path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app  # Import your FastAPI app

# Create a test client
client = TestClient(app)

USER_ID = "test-user-123"
OTHER_USER_ID = "other-user-456"
TASK_ID = "a1b2c3d4-e5f6-7890-1234-567890abcdef"


@pytest.fixture
def mock_db_session():
    """Fixture to mock the database session."""
    with patch("src.api.v1.endpoints.tasks.get_db_session") as mock_get_db:
        mock_session = MagicMock()
        # Mock the repository and its methods if needed
        mock_repo = MagicMock()
        mock_session.return_value = mock_repo
        mock_get_db.return_value = mock_session
        yield mock_session

def test_get_tasks_no_token(mock_db_session):
    """
    Test that accessing a protected endpoint without a token fails.
    """
    response = client.get(f"/api/v1/{USER_ID}/tasks")
    assert response.status_code == 401  # HTTPBearer's auto_error for missing credentials

@patch('src.middleware.jwt.JWTUtil.verify_token')
def test_get_tasks_invalid_token(mock_verify_token, mock_db_session):
    """
    Test that accessing a protected endpoint with an invalid token fails.
    """
    mock_verify_token.side_effect = Exception("Invalid token")
    response = client.get(
        f"/api/v1/{USER_ID}/tasks",
        headers={"Authorization": "Bearer bogus-token"}
    )
    assert response.status_code == 401

@patch('src.middleware.jwt.JWTUtil.verify_token')
def test_get_tasks_valid_token_correct_user(mock_verify_token, mock_db_session):
    """
    Test that accessing a protected endpoint with a valid token for the correct user succeeds.
    """
    mock_verify_token.return_value = {"user": {"id": USER_ID}}
    
    # Mock the repository method to return some tasks
    mock_repo = mock_db_session.return_value
    mock_repo.get_tasks_by_user_id.return_value = [] # Return an empty list for simplicity

    response = client.get(
        f"/api/v1/{USER_ID}/tasks",
        headers={"Authorization": "Bearer valid-token"}
    )
    assert response.status_code == 200
    assert response.json() == []

@patch('src.middleware.jwt.JWTUtil.verify_token')
def test_get_tasks_valid_token_wrong_user(mock_verify_token, mock_db_session):
    """
    Test that accessing a protected endpoint with a valid token for the wrong user is forbidden.
    """
    mock_verify_token.return_value = {"user": {"id": OTHER_USER_ID}}
    response = client.get(
        f"/api/v1/{USER_ID}/tasks",
        headers={"Authorization": "Bearer valid-token"}
    )
    assert response.status_code == 403 # From verify_user_access
    assert response.json() == {"detail": "Access denied: You can only access your own resources"}

@patch('src.middleware.jwt.JWTUtil.verify_token')
def test_create_task_valid_token(mock_verify_token, mock_db_session):
    """
    Test creating a task with a valid token.
    """
    mock_verify_token.return_value = {"user": {"id": USER_ID}}
    
    task_data = {"title": "Test Task", "description": "Test Description"}
    
    # Mock the repository method to return a created task
    mock_repo = mock_db_session.return_value
    from src.database.models import Task
    from datetime import datetime
    from uuid import uuid4
    
    created_task = Task(
        id=uuid4(), 
        title=task_data["title"], 
        description=task_data["description"],
        completed=False,
        user_id=USER_ID,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    mock_repo.create_task_for_user.return_value = created_task

    response = client.post(
        f"/api/v1/{USER_ID}/tasks",
        headers={"Authorization": "Bearer valid-token"},
        json=task_data
    )
    
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]

