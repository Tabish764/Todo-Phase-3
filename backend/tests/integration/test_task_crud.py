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


def test_full_crud_operations_integration(client, clean_db):
    """
    Integration test that verifies the complete CRUD cycle for tasks.
    This test ensures all operations work together as expected.
    """
    # CREATE: Add a new task
    create_data = {
        "title": "Integration Test Task",
        "description": "Integration test description"
    }
    create_response = client.post("/tasks", json=create_data)

    assert create_response.status_code == 201
    created_task = create_response.json()

    # Verify the created task has required fields
    assert "id" in created_task
    assert created_task["title"] == "Integration Test Task"
    assert created_task["description"] == "Integration test description"
    assert created_task["completed"] is False

    task_id = created_task["id"]

    # READ: Get all tasks and verify the created task is there
    read_response = client.get("/tasks")
    assert read_response.status_code == 200

    tasks = read_response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["title"] == "Integration Test Task"

    # UPDATE: Modify the task
    update_data = {
        "title": "Updated Integration Test Task",
        "description": "Updated integration test description",
        "completed": True
    }
    update_response = client.put(f"/tasks/{task_id}", json=update_data)

    assert update_response.status_code == 200
    updated_task = update_response.json()

    # Verify the task was updated
    assert updated_task["id"] == task_id
    assert updated_task["title"] == "Updated Integration Test Task"
    assert updated_task["description"] == "Updated integration test description"
    assert updated_task["completed"] is True

    # READ: Verify the update by getting all tasks again
    read_response_after_update = client.get("/tasks")
    assert read_response_after_update.status_code == 200

    tasks_after_update = read_response_after_update.json()
    assert len(tasks_after_update) == 1
    assert tasks_after_update[0]["id"] == task_id
    assert tasks_after_update[0]["title"] == "Updated Integration Test Task"
    assert tasks_after_update[0]["completed"] is True

    # DELETE: Remove the task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    # READ: Verify the task is gone
    read_response_after_delete = client.get("/tasks")
    assert read_response_after_delete.status_code == 200

    tasks_after_delete = read_response_after_delete.json()
    assert len(tasks_after_delete) == 0


def test_multiple_tasks_crud_integration(client, clean_db):
    """
    Integration test that verifies CRUD operations with multiple tasks.
    """
    # CREATE: Add multiple tasks
    task1_data = {
        "title": "First Integration Task",
        "description": "First task description"
    }
    task2_data = {
        "title": "Second Integration Task",
        "description": "Second task description"
    }

    create_response1 = client.post("/tasks", json=task1_data)
    create_response2 = client.post("/tasks", json=task2_data)

    assert create_response1.status_code == 201
    assert create_response2.status_code == 201

    task1 = create_response1.json()
    task2 = create_response2.json()

    task1_id = task1["id"]
    task2_id = task2["id"]

    # READ: Verify both tasks exist
    read_response = client.get("/tasks")
    assert read_response.status_code == 200

    tasks = read_response.json()
    assert len(tasks) == 2

    # Find both tasks in the list
    task_ids = [task["id"] for task in tasks]
    assert task1_id in task_ids
    assert task2_id in task_ids

    # UPDATE: Modify one task
    update_data = {
        "title": "Updated First Integration Task",
        "completed": True
    }
    update_response = client.put(f"/tasks/{task1_id}", json=update_data)
    assert update_response.status_code == 200

    updated_task = update_response.json()
    assert updated_task["title"] == "Updated First Integration Task"
    assert updated_task["completed"] is True

    # READ: Verify both tasks still exist, with one updated
    read_response_after_update = client.get("/tasks")
    assert read_response_after_update.status_code == 200

    tasks_after_update = read_response_after_update.json()
    assert len(tasks_after_update) == 2

    # Find the updated task and verify changes
    updated_task_found = next((t for t in tasks_after_update if t["id"] == task1_id), None)
    assert updated_task_found is not None
    assert updated_task_found["title"] == "Updated First Integration Task"
    assert updated_task_found["completed"] is True

    # Find the unmodified task and verify it's unchanged
    unmodified_task_found = next((t for t in tasks_after_update if t["id"] == task2_id), None)
    assert unmodified_task_found is not None
    assert unmodified_task_found["title"] == "Second Integration Task"
    assert unmodified_task_found["completed"] is False

    # DELETE: Remove one task
    delete_response = client.delete(f"/tasks/{task2_id}")
    assert delete_response.status_code == 204

    # READ: Verify only one task remains
    read_response_after_delete = client.get("/tasks")
    assert read_response_after_delete.status_code == 200

    tasks_after_delete = read_response_after_delete.json()
    assert len(tasks_after_delete) == 1
    assert tasks_after_delete[0]["id"] == task1_id
    assert tasks_after_delete[0]["title"] == "Updated First Integration Task"


def test_crud_error_handling_integration(client, clean_db):
    """
    Integration test that verifies error handling across CRUD operations.
    """
    # Attempt to update a non-existent task
    nonexistent_id = "nonexistent-task-id"
    update_data = {
        "title": "Should not work",
        "completed": True
    }
    update_response = client.put(f"/tasks/{nonexistent_id}", json=update_data)
    assert update_response.status_code == 404

    # Attempt to delete a non-existent task
    delete_response = client.delete(f"/tasks/{nonexistent_id}")
    assert delete_response.status_code == 404

    # Create a valid task first
    create_data = {
        "title": "Test Task for Error Handling",
        "description": "Task to test error handling"
    }
    create_response = client.post("/tasks", json=create_data)
    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Verify the task exists
    read_response = client.get("/tasks")
    assert read_response.status_code == 200
    tasks = read_response.json()
    assert len(tasks) == 1

    # Delete the task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    # Try to update the deleted task (should fail)
    update_data = {
        "title": "Should fail - task deleted"
    }
    retry_update_response = client.put(f"/tasks/{task_id}", json=update_data)
    assert retry_update_response.status_code == 404

    # Verify no tasks remain
    final_read_response = client.get("/tasks")
    assert final_read_response.status_code == 200
    final_tasks = final_read_response.json()
    assert len(final_tasks) == 0