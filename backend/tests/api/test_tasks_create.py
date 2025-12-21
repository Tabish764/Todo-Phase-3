import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.memory_db import db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def clean_db():
    # Clean up any existing tasks
    db._tasks.clear()
    yield
    # Clean up after test
    db._tasks.clear()


def test_post_tasks_success(client, clean_db):
    """Test that POST /tasks creates a new task with 201 status"""
    task_data = {
        "title": "New Test Task",
        "description": "Test Description"
    }

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 201
    data = response.json()

    # Verify response structure
    assert "id" in data
    assert data["title"] == "New Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert "created_at" in data
    assert "updated_at" in data

    # Verify the task was actually saved
    get_response = client.get("/tasks")
    assert get_response.status_code == 200
    tasks = get_response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == data["id"]
    assert tasks[0]["title"] == "New Test Task"


def test_post_tasks_minimal_data(client, clean_db):
    """Test that POST /tasks works with minimal required data (just title)"""
    task_data = {
        "title": "Minimal Task"
    }

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 201
    data = response.json()

    # Verify response structure
    assert "id" in data
    assert data["title"] == "Minimal Task"
    assert data["description"] is None  # Optional field should be None
    assert data["completed"] is False
    assert "created_at" in data
    assert "updated_at" in data


def test_post_tasks_missing_title(client, clean_db):
    """Test that POST /tasks returns 400 when title is missing"""
    task_data = {
        "description": "Task without title"
    }

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 422  # Validation error from Pydantic


def test_post_tasks_invalid_title_length(client, clean_db):
    """Test that POST /tasks returns 400 when title is too short or too long"""
    # Test too short title
    task_data_short = {
        "title": ""  # Empty title
    }

    response_short = client.post("/tasks", json=task_data_short)
    assert response_short.status_code == 422  # Validation error

    # Test too long title
    long_title = "t" * 201  # 201 characters, exceeding limit
    task_data_long = {
        "title": long_title
    }

    response_long = client.post("/tasks", json=task_data_long)
    assert response_long.status_code == 422  # Validation error