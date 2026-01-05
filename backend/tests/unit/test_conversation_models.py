import pytest
from datetime import datetime
from backend.src.models.conversation import Conversation, Message


def test_conversation_model_creation():
    """Test creating a conversation model instance"""
    conversation = Conversation(
        user_id="user123",
        title="Test Conversation"
    )

    assert conversation.user_id == "user123"
    assert conversation.title == "Test Conversation"
    assert conversation.id is None  # ID will be set by the database
    assert isinstance(conversation.created_at, datetime)
    assert isinstance(conversation.updated_at, datetime)


def test_conversation_model_defaults():
    """Test conversation model with default values"""
    conversation = Conversation(
        user_id="user123"
    )

    assert conversation.user_id == "user123"
    assert conversation.title is None
    assert isinstance(conversation.created_at, datetime)
    assert isinstance(conversation.updated_at, datetime)


def test_message_model_creation():
    """Test creating a message model instance"""
    message = Message(
        conversation_id=1,
        user_id="user123",
        role="user",
        content="Hello, world!"
    )

    assert message.conversation_id == 1
    assert message.user_id == "user123"
    assert message.role == "user"
    assert message.content == "Hello, world!"
    assert message.tool_calls is None
    assert isinstance(message.created_at, datetime)


def test_message_model_with_tool_calls():
    """Test message model with tool calls"""
    message = Message(
        conversation_id=1,
        user_id="user123",
        role="assistant",
        content="Here is the result",
        tool_calls='{"function": "get_user_todos", "arguments": {}}'
    )

    assert message.conversation_id == 1
    assert message.user_id == "user123"
    assert message.role == "assistant"
    assert message.content == "Here is the result"
    assert message.tool_calls == '{"function": "get_user_todos", "arguments": {}}'


def test_message_model_role_validation():
    """Test that message role validation works (though this is handled at DB level)"""
    # Test valid roles
    for role in ["user", "assistant", "system"]:
        message = Message(
            conversation_id=1,
            user_id="user123",
            role=role,
            content=f"Message as {role}"
        )
        assert message.role == role


def test_message_model_required_fields():
    """Test that required fields are properly set"""
    message = Message(
        conversation_id=1,
        user_id="user123",
        role="user",
        content="Test content"
    )

    assert message.conversation_id == 1
    assert message.user_id == "user123"
    assert message.role == "user"
    assert message.content == "Test content"
    assert message.content != ""  # Content should not be empty


if __name__ == "__main__":
    test_conversation_model_creation()
    test_conversation_model_defaults()
    test_message_model_creation()
    test_message_model_with_tool_calls()
    test_message_model_role_validation()
    test_message_model_required_fields()
    print("All tests passed!")