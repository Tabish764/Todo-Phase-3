"""
Input Validation Utilities

This module provides utility functions for validating MCP tool inputs.
"""
from typing import Dict, Any, Union
from pydantic import ValidationError
import json


def validate_input_against_schema(input_data: Dict[str, Any], schema: Dict[str, Any]) -> tuple[bool, Union[str, None]]:
    """
    Validate input data against a JSON schema.

    Args:
        input_data: The input data to validate
        schema: The JSON schema to validate against

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Basic validation using the schema structure
        required_fields = schema.get("required", [])

        # Check required fields
        for field in required_fields:
            if field not in input_data:
                return False, f"Missing required field: {field}"

        # Validate field types based on schema
        properties = schema.get("properties", {})
        for field, value in input_data.items():
            if field in properties:
                expected_type = properties[field].get("type")

                # Map JSON types to Python types for basic validation
                if expected_type == "string" and not isinstance(value, str):
                    return False, f"Field {field} must be a string, got {type(value).__name__}"
                elif expected_type == "integer" and not isinstance(value, int):
                    return False, f"Field {field} must be an integer, got {type(value).__name__}"
                elif expected_type == "boolean" and not isinstance(value, bool):
                    return False, f"Field {field} must be a boolean, got {type(value).__name__}"
                elif expected_type == "array" and not isinstance(value, list):
                    return False, f"Field {field} must be an array, got {type(value).__name__}"
                elif expected_type == "object" and not isinstance(value, dict):
                    return False, f"Field {field} must be an object, got {type(value).__name__}"

        # Additional validation for specific field constraints
        for field, value in input_data.items():
            if field in properties:
                field_props = properties[field]

                # Check string length constraints
                if properties[field].get("type") == "string":
                    max_length = field_props.get("maxLength")
                    if max_length and len(str(value)) > max_length:
                        return False, f"Field {field} exceeds maximum length of {max_length}"

        return True, None

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_add_task_input(input_data: Dict[str, Any]) -> tuple[bool, Union[str, None]]:
    """
    Validate input for add_task tool.

    Args:
        input_data: The input data to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    if "user_id" not in input_data:
        return False, "User ID is required"

    if "title" not in input_data:
        return False, "Task title is required"

    # Validate field types
    if not isinstance(input_data["user_id"], str):
        return False, "user_id must be a string"

    if not isinstance(input_data["title"], str):
        return False, "title must be a string"

    # Validate title is not empty
    if not input_data["title"].strip():
        return False, "Task title cannot be empty"

    # Validate optional description if provided
    if "description" in input_data and input_data["description"] is not None:
        if not isinstance(input_data["description"], str):
            return False, "description must be a string if provided"

    return True, None


def validate_list_tasks_input(input_data: Dict[str, Any]) -> tuple[bool, Union[str, None]]:
    """
    Validate input for list_tasks tool.

    Args:
        input_data: The input data to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    if "user_id" not in input_data:
        return False, "User ID is required"

    # Validate field types
    if not isinstance(input_data["user_id"], str):
        return False, "user_id must be a string"

    # Validate optional status field if provided
    if "status" in input_data and input_data["status"] is not None:
        if not isinstance(input_data["status"], str):
            return False, "status must be a string if provided"

        allowed_status_values = ["all", "pending", "completed"]
        if input_data["status"] not in allowed_status_values:
            return False, f"status must be one of {allowed_status_values}"

    return True, None


def validate_complete_task_input(input_data: Dict[str, Any]) -> tuple[bool, Union[str, None]]:
    """
    Validate input for complete_task tool.

    Args:
        input_data: The input data to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    if "user_id" not in input_data:
        return False, "User ID is required"

    if "task_id" not in input_data:
        return False, "Task ID is required"

    # Validate field types
    if not isinstance(input_data["user_id"], str):
        return False, "user_id must be a string"

    if not isinstance(input_data["task_id"], int):
        return False, "task_id must be an integer"

    # Validate task_id is positive
    if input_data["task_id"] <= 0:
        return False, "task_id must be a positive integer"

    return True, None


def validate_delete_task_input(input_data: Dict[str, Any]) -> tuple[bool, Union[str, None]]:
    """
    Validate input for delete_task tool.

    Args:
        input_data: The input data to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    if "user_id" not in input_data:
        return False, "User ID is required"

    if "task_id" not in input_data:
        return False, "Task ID is required"

    # Validate field types
    if not isinstance(input_data["user_id"], str):
        return False, "user_id must be a string"

    if not isinstance(input_data["task_id"], int):
        return False, "task_id must be an integer"

    # Validate task_id is positive
    if input_data["task_id"] <= 0:
        return False, "task_id must be a positive integer"

    return True, None


def validate_update_task_input(input_data: Dict[str, Any]) -> tuple[bool, Union[str, None]]:
    """
    Validate input for update_task tool.

    Args:
        input_data: The input data to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    if "user_id" not in input_data:
        return False, "User ID is required"

    if "task_id" not in input_data:
        return False, "Task ID is required"

    # Check that at least one optional field is provided
    update_fields = ["title", "description"]
    if not any(field in input_data for field in update_fields):
        return False, "At least one field (title or description) must be provided for update"

    # Validate field types
    if not isinstance(input_data["user_id"], str):
        return False, "user_id must be a string"

    if not isinstance(input_data["task_id"], int):
        return False, "task_id must be an integer"

    # Validate task_id is positive
    if input_data["task_id"] <= 0:
        return False, "task_id must be a positive integer"

    # Validate optional title if provided
    if "title" in input_data and input_data["title"] is not None:
        if not isinstance(input_data["title"], str):
            return False, "title must be a string if provided"
        if not input_data["title"].strip():
            return False, "Task title cannot be empty"

    # Validate optional description if provided
    if "description" in input_data and input_data["description"] is not None:
        if not isinstance(input_data["description"], str):
            return False, "description must be a string if provided"

    return True, None