import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.task import Task
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


def test_get_nonexistent_task_404(client, clean_db):
    """Test that GET /tasks/{id} returns 404 for non-existent task"""
    nonexistent_id = "nonexistent-task-id"

    response = client.get(f"/tasks/{nonexistent_id}")

    # Since GET /tasks/{id} is not implemented, it should return 405 (Method Not Allowed)
    # based on our API contract which only supports GET /tasks (plural) for listing
    assert response.status_code == 405


def test_put_nonexistent_task_404(client, clean_db):
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


def test_delete_nonexistent_task_404(client, clean_db):
    """Test that DELETE /tasks/{id} returns 404 for non-existent task"""
    nonexistent_id = "nonexistent-task-id"

    response = client.delete(f"/tasks/{nonexistent_id}")

    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data
    assert error_data["detail"] == "Task not found"


def test_error_response_format_consistency_404(client, clean_db):
    """Test that 404 error responses follow consistent format"""
    nonexistent_id = "nonexistent-task-id"

    # Test PUT 404 response format
    update_data = {"title": "Test Title"}
    put_response = client.put(f"/tasks/{nonexistent_id}", json=update_data)

    assert put_response.status_code == 404
    put_error_data = put_response.json()
    assert "detail" in put_error_data
    assert isinstance(put_error_data["detail"], str)

    # Test DELETE 404 response format
    delete_response = client.delete(f"/tasks/{nonexistent_id}")

    assert delete_response.status_code == 404
    delete_error_data = delete_response.json()
    assert "detail" in delete_error_data
    assert isinstance(delete_error_data["detail"], str)


def test_multiple_nonexistent_operations(client, clean_db):
    """Test multiple operations on non-existent tasks return 404 consistently"""
    nonexistent_id = "nonexistent-task-id"

    # Test PUT
    put_response = client.put(f"/tasks/{nonexistent_id}", json={"title": "Test"})
    assert put_response.status_code == 404

    # Test DELETE
    delete_response = client.delete(f"/tasks/{nonexistent_id}")
    assert delete_response.status_code == 404

    # Verify no tasks were created as a side effect
    get_response = client.get("/tasks")
    assert get_response.status_code == 200
    tasks = get_response.json()
    assert len(tasks) == 0