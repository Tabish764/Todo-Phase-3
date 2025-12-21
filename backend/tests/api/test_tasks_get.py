import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.task import Task
from src.database.memory_db import db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def setup_test_data():
    # Clean up any existing tasks
    db._tasks.clear()

    # Create test tasks
    task1 = Task.create(title="Test Task 1", description="Test Description 1")
    task2 = Task.create(title="Test Task 2", description="Test Description 2")

    db.create_task(task1)
    db.create_task(task2)

    yield

    # Clean up after test
    db._tasks.clear()


def test_get_tasks_success(client, setup_test_data):
    """Test that GET /tasks returns all tasks with 200 status"""
    response = client.get("/tasks")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    # Check first task
    first_task = data[0]
    assert "id" in first_task
    assert first_task["title"] == "Test Task 1"
    assert first_task["description"] == "Test Description 1"
    assert "created_at" in first_task
    assert "updated_at" in first_task


def test_get_tasks_empty_list(client):
    """Test that GET /tasks returns empty list when no tasks exist"""
    # Ensure no tasks exist
    db._tasks.clear()

    response = client.get("/tasks")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 0