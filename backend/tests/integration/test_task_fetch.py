import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.task import Task
from src.database.memory_db import db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def setup_tasks():
    # Clean up any existing tasks
    db._tasks.clear()

    # Create test tasks
    task1 = Task.create(title="Integration Test Task 1", description="Integration Description 1")
    task2 = Task.create(title="Integration Test Task 2", description="Integration Description 2")
    task3 = Task.create(title="Integration Test Task 3", description="Integration Description 3")

    db.create_task(task1)
    db.create_task(task2)
    db.create_task(task3)

    yield

    # Clean up after test
    db._tasks.clear()


def test_full_task_fetch_integration(client, setup_tasks):
    """
    Integration test for task fetching from backend to frontend API contract.
    This test verifies the complete flow from the API endpoint to the data retrieval.
    """
    # Test fetching all tasks
    response = client.get("/tasks")

    assert response.status_code == 200

    # Verify response structure
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 3

    # Verify each task has the required fields
    for task in tasks:
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "created_at" in task
        assert "updated_at" in task

        # Verify data types
        assert isinstance(task["id"], str)
        assert isinstance(task["title"], str)
        assert isinstance(task["description"], str) or task["description"] is None
        assert isinstance(task["completed"], bool)
        assert isinstance(task["created_at"], str)
        assert isinstance(task["updated_at"], str)

    # Verify specific task data
    titles = [task["title"] for task in tasks]
    assert "Integration Test Task 1" in titles
    assert "Integration Test Task 2" in titles
    assert "Integration Test Task 3" in titles


def test_frontend_backend_connection_integration(client, setup_tasks):
    """
    Test that simulates the frontend-backend connection for task fetching.
    Verifies that the backend API provides the stable contract the frontend expects.
    """
    # Simulate frontend requesting tasks
    response = client.get("/tasks")

    assert response.status_code == 200

    tasks = response.json()

    # Verify the API contract that frontend expects
    for task in tasks:
        # Frontend expects these specific fields
        expected_fields = ["id", "title", "description", "completed", "created_at", "updated_at"]
        for field in expected_fields:
            assert field in task, f"Field {field} missing from task response"

        # Verify title constraints (1-200 characters)
        assert 1 <= len(task["title"]) <= 200, f"Title length constraint violated: '{task['title']}'"

        # Verify completed is boolean
        assert isinstance(task["completed"], bool), f"Completed field should be boolean, got {type(task['completed'])}"