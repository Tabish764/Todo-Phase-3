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
    task = Task.create(title="Task to Delete", description="Description to delete")
    created_task = db.create_task(task)

    yield created_task.id  # Return the task ID

    # Clean up after test
    db._tasks.clear()


def test_delete_tasks_success(client, setup_single_task):
    """Test that DELETE /tasks/{id} removes a task with 204 status"""
    task_id = setup_single_task

    # Verify task exists before deletion
    get_response = client.get("/tasks")
    assert get_response.status_code == 200
    tasks_before = get_response.json()
    assert len(tasks_before) == 1
    assert tasks_before[0]["id"] == task_id

    # Delete the task
    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""  # 204 No Content should have empty body

    # Verify task no longer exists
    get_response_after = client.get("/tasks")
    assert get_response_after.status_code == 200
    tasks_after = get_response_after.json()
    assert len(tasks_after) == 0


def test_delete_tasks_nonexistent(client):
    """Test that DELETE /tasks/{id} returns 404 for non-existent task"""
    nonexistent_id = "nonexistent-task-id"

    response = client.delete(f"/tasks/{nonexistent_id}")

    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data
    assert error_data["detail"] == "Task not found"


def test_delete_tasks_then_verify_gone(client, setup_single_task):
    """Test that after DELETE, the task cannot be accessed anymore"""
    task_id = setup_single_task

    # Verify task exists before deletion
    response_before = client.get(f"/tasks/{task_id}")
    # Note: Our API doesn't support GET /tasks/{id}, so we'll test by seeing if it's in the list
    list_response_before = client.get("/tasks")
    assert list_response_before.status_code == 200
    tasks_before = list_response_before.json()
    assert len(tasks_before) == 1

    # Delete the task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    # Verify task is gone by checking the list
    list_response_after = client.get("/tasks")
    assert list_response_after.status_code == 200
    tasks_after = list_response_after.json()
    assert len(tasks_after) == 0


def test_delete_multiple_tasks(client):
    """Test that multiple tasks can be deleted individually"""
    # Clean up any existing tasks
    db._tasks.clear()

    # Create multiple test tasks
    task1 = Task.create(title="Task 1 to Delete", description="Description 1")
    task2 = Task.create(title="Task 2 to Delete", description="Description 2")
    created_task1 = db.create_task(task1)
    created_task2 = db.create_task(task2)

    # Verify both tasks exist
    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    tasks_before = list_response.json()
    assert len(tasks_before) == 2

    # Delete first task
    response1 = client.delete(f"/tasks/{created_task1.id}")
    assert response1.status_code == 204

    # Verify only one task remains
    list_response_after_1 = client.get("/tasks")
    assert list_response_after_1.status_code == 200
    tasks_after_1 = list_response_after_1.json()
    assert len(tasks_after_1) == 1

    # Delete second task
    response2 = client.delete(f"/tasks/{created_task2.id}")
    assert response2.status_code == 204

    # Verify no tasks remain
    list_response_after_2 = client.get("/tasks")
    assert list_response_after_2.status_code == 200
    tasks_after_2 = list_response_after_2.json()
    assert len(tasks_after_2) == 0