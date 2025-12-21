import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.task import Task
from src.database.memory_db import db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def setup_single_task():
    # Clean up any existing tasks
    db._tasks.clear()

    # Create a test task
    task = Task.create(title="Original Task", description="Original Description")
    db.create_task(task)

    yield task.id  # Return the task ID

    # Clean up after test
    db._tasks.clear()


def test_put_tasks_success(client, setup_single_task):
    """Test that PUT /tasks/{id} updates a task with 200 status"""
    task_id = setup_single_task
    update_data = {
        "title": "Updated Task Title",
        "description": "Updated Description",
        "completed": True
    }

    response = client.put(f"/tasks/{task_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert data["id"] == task_id
    assert data["title"] == "Updated Task Title"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True
    assert "created_at" in data
    assert "updated_at" in data
    # Verify updated_at is newer than created_at
    assert data["updated_at"] >= data["created_at"]


def test_put_tasks_partial_update(client, setup_single_task):
    """Test that PUT /tasks/{id} can update individual fields"""
    task_id = setup_single_task
    update_data = {
        "title": "Partially Updated Task Title"
        # Only updating title, other fields should remain unchanged
    }

    response = client.put(f"/tasks/{task_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()

    # Verify only the updated field changed
    assert data["id"] == task_id
    assert data["title"] == "Partially Updated Task Title"
    assert data["description"] == "Original Description"  # Should remain unchanged
    assert data["completed"] is False  # Should remain unchanged
    assert "created_at" in data
    assert "updated_at" in data


def test_put_tasks_nonexistent(client):
    """Test that PUT /tasks/{id} returns 404 for non-existent task"""
    nonexistent_id = "nonexistent-task-id"
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description"
    }

    response = client.put(f"/tasks/{nonexistent_id}", json=update_data)

    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data
    assert error_data["detail"] == "Task not found"


def test_put_tasks_invalid_title(client, setup_single_task):
    """Test that PUT /tasks/{id} returns 422 for invalid title"""
    task_id = setup_single_task
    update_data = {
        "title": "",  # Invalid: empty title
        "description": "Valid description"
    }

    response = client.put(f"/tasks/{task_id}", json=update_data)

    assert response.status_code == 422  # Validation error


def test_put_tasks_valid_completed_status(client, setup_single_task):
    """Test that PUT /tasks/{id} properly updates completed status"""
    task_id = setup_single_task

    # First, ensure the task is not completed
    initial_response = client.get(f"/tasks/{task_id}")
    assert initial_response.status_code == 405  # GET not supported for single task

    # Update to completed
    update_data = {
        "completed": True
    }
    response = client.put(f"/tasks/{task_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True

    # Update back to not completed
    update_data = {
        "completed": False
    }
    response = client.put(f"/tasks/{task_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False