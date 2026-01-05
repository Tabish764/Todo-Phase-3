"""Unit tests for message model validation."""
import pytest
from datetime import datetime
from backend.models.message import Message, MessageCreate, MessageRole


def test_message_model_validation():
    """Test message model field validation."""
    # Test valid message creation
    message = Message(
        conversation_id=1,
        user_id="testuser",
        role=MessageRole.user,
        content="Test message content",
        created_at=datetime.utcnow()
    )
    
    assert message.conversation_id == 1
    assert message.user_id == "testuser"
    assert message.role == MessageRole.user
    assert message.content == "Test message content"


def test_message_create_model_validation():
    """Test MessageCreate model validation."""
    # Test valid message creation
    message_create = MessageCreate(
        conversation_id=1,
        user_id="testuser",
        role=MessageRole.user,
        content="Test message content"
    )
    
    assert message_create.conversation_id == 1
    assert message_create.user_id == "testuser"
    assert message_create.role == MessageRole.user
    assert message_create.content == "Test message content"


def test_message_content_validation():
    """Test message content validation."""
    # Test that content cannot be empty
    with pytest.raises(ValueError):
        MessageCreate(
            conversation_id=1,
            user_id="testuser",
            role=MessageRole.user,
            content=""  # Empty content should fail validation
        )


def test_message_role_validation():
    """Test message role validation."""
    # Test user role
    message_user = MessageCreate(
        conversation_id=1,
        user_id="testuser",
        role=MessageRole.user,
        content="User message"
    )
    assert message_user.role == MessageRole.user
    
    # Test assistant role
    message_assistant = MessageCreate(
        conversation_id=1,
        user_id="testuser",
        role=MessageRole.assistant,
        content="Assistant message"
    )
    assert message_assistant.role == MessageRole.assistant


def test_message_optional_fields():
    """Test optional fields in message model."""
    # Test with tool_calls as None (optional)
    message = MessageCreate(
        conversation_id=1,
        user_id="testuser",
        role=MessageRole.assistant,
        content="Message with no tools"
    )
    
    assert message.conversation_id == 1
    assert message.user_id == "testuser"
    assert message.role == MessageRole.assistant
    assert message.content == "Message with no tools"
    # tool_calls is optional and defaults to None
