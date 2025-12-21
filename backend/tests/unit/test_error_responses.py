import pytest
from fastapi import HTTPException
from src.api.v1.endpoints.tasks import handle_not_found
from src.models.task import Task


def test_handle_not_found_success():
    """Test that handle_not_found returns the task when it exists"""
    task = Task.create(title="Test Task", description="Test Description")

    result = handle_not_found(task)

    assert result == task


def test_handle_not_found_raises_404():
    """Test that handle_not_found raises HTTPException with 404 status when task is None"""
    with pytest.raises(HTTPException) as exc_info:
        handle_not_found(None)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Task not found"


def test_error_response_format():
    """Test that error responses follow the expected format"""
    with pytest.raises(HTTPException) as exc_info:
        handle_not_found(None)

    # Verify the exception has the expected structure
    assert hasattr(exc_info.value, 'status_code')
    assert exc_info.value.status_code == 404
    assert hasattr(exc_info.value, 'detail')
    assert exc_info.value.detail == "Task not found"


def test_multiple_error_scenarios():
    """Test various scenarios that should raise 404 errors"""
    # Test with None
    with pytest.raises(HTTPException) as exc_info:
        handle_not_found(None)
    assert exc_info.value.status_code == 404

    # Test that valid task doesn't raise error
    task = Task.create(title="Valid Task", description="Description")
    result = handle_not_found(task)
    assert result is not None
    assert result.title == "Valid Task"