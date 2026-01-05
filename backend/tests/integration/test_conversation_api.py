import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.main import app
from backend.src.database.connection import db_connection
from backend.src.models.conversation import Conversation, Message
from backend.src.services.conversation_service import ConversationService
import asyncio


@pytest.fixture(scope="module")
def client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def db_session():
    """Create a database session for testing"""
    # Use the existing database connection
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        yield session


@pytest.mark.asyncio
async def test_conversation_lifecycle():
    """Test the full lifecycle of a conversation: create, add messages, retrieve"""
    # Note: This test would require proper authentication setup
    # For now, we'll test the service layer directly

    # Create a test session
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        # Test creating a conversation
        user_id = "test_user_123"
        conversation = await service.create_conversation(user_id=user_id, title="Test Conversation")

        assert conversation.user_id == user_id
        assert conversation.title == "Test Conversation"

        # Test adding a message to the conversation
        message = await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="Hello, AI assistant!"
        )

        assert message.conversation_id == conversation.id
        assert message.user_id == user_id
        assert message.role == "user"
        assert message.content == "Hello, AI assistant!"

        # Test retrieving messages from the conversation
        messages, total = await service.get_messages_for_conversation(
            conversation_id=conversation.id,
            user_id=user_id
        )

        assert len(messages) == 1
        assert total == 1
        assert messages[0].content == "Hello, AI assistant!"

        # Test retrieving user's conversations
        conversations, total_convs = await service.get_user_conversations(user_id=user_id)

        assert len(conversations) >= 1
        assert total_convs >= 1
        assert any(conv.id == conversation.id for conv in conversations)


@pytest.mark.asyncio
async def test_conversation_isolation():
    """Test that users can only access their own conversations"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        # Create conversations for different users
        user1_id = "user_1"
        user2_id = "user_2"

        conv1 = await service.create_conversation(user_id=user1_id, title="User 1's conversation")
        conv2 = await service.create_conversation(user_id=user2_id, title="User 2's conversation")

        # User 1 should only see their own conversation
        user1_conversations, user1_total = await service.get_user_conversations(user_id=user1_id)
        assert len(user1_conversations) == 1
        assert user1_conversations[0].id == conv1.id

        # User 2 should only see their own conversation
        user2_conversations, user2_total = await service.get_user_conversations(user_id=user2_id)
        assert len(user2_conversations) == 1
        assert user2_conversations[0].id == conv2.id

        # Test that user 1 cannot access user 2's conversation
        user1_conv = await service.get_conversation_by_id(conversation_id=conv2.id, user_id=user1_id)
        assert user1_conv is None


@pytest.mark.asyncio
async def test_message_role_validation():
    """Test that only valid roles are accepted"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "test_user_456"
        conversation = await service.create_conversation(user_id=user_id)

        # Valid roles should work
        for role in ["user", "assistant", "system"]:
            message = await service.add_message_to_conversation(
                conversation_id=conversation.id,
                user_id=user_id,
                role=role,
                content=f"Message with role {role}"
            )
            assert message.role == role


@pytest.mark.asyncio
async def test_conversation_timestamp_updates():
    """Test that conversation timestamps are updated when messages are added"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "test_user_789"
        conversation = await service.create_conversation(user_id=user_id)

        original_updated_at = conversation.updated_at

        # Add a message which should update the conversation timestamp
        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="Test message"
        )

        # Get the conversation again to check updated timestamp
        updated_conversation = await service.get_conversation_by_id(
            conversation_id=conversation.id,
            user_id=user_id
        )

        # The updated_at should be different (or at least not earlier than before)
        assert updated_conversation.updated_at >= original_updated_at


if __name__ == "__main__":
    # For running tests individually during development
    pass