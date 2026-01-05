import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database.connection import db_connection
from backend.src.models.conversation import Conversation, Message
from backend.src.services.conversation_service import ConversationService
from datetime import datetime


@pytest.mark.asyncio
async def test_conversation_persistence_across_sessions():
    """
    Test conversation persistence across sessions:
    Given a user has had previous conversations with the AI chatbot,
    When the user accesses the chat interface,
    Then the user sees their recent conversation history in chronological order
    """
    # First session: Create a conversation and add messages
    engine = db_connection.engine
    async with AsyncSession(engine) as session1:
        service1 = ConversationService(session1)

        user_id = "test_user_persistence"

        # Create first conversation
        conv1 = await service1.create_conversation(user_id=user_id, title="First Conversation")

        # Add some messages to the first conversation
        await service1.add_message_to_conversation(
            conversation_id=conv1.id,
            user_id=user_id,
            role="user",
            content="Hello, first conversation!"
        )

        # Wait a bit to ensure different timestamps
        import asyncio
        await asyncio.sleep(0.01)

        # Create second conversation
        conv2 = await service1.create_conversation(user_id=user_id, title="Second Conversation")

        # Add messages to the second conversation
        await service1.add_message_to_conversation(
            conversation_id=conv2.id,
            user_id=user_id,
            role="user",
            content="Hello, second conversation!"
        )

        # Commit and close first session
        await session1.commit()

    # Simulate a new session: Create a new session to test persistence
    async with AsyncSession(engine) as session2:
        service2 = ConversationService(session2)

        # Retrieve user's conversations - they should be sorted by most recent activity
        conversations, total = await service2.get_user_conversations(user_id=user_id)

        # Verify that both conversations are retrieved
        assert len(conversations) == 2
        assert total == 2

        # Verify that conversations are sorted by updated_at (most recent first)
        # Since we created conv2 after conv1, conv2 should be first in the list
        assert conversations[0].id == conv2.id
        assert conversations[1].id == conv1.id

        # Verify that we can retrieve messages from both conversations
        messages1, total1 = await service2.get_messages_for_conversation(
            conversation_id=conv1.id,
            user_id=user_id
        )
        assert len(messages1) == 1
        assert messages1[0].content == "Hello, first conversation!"

        messages2, total2 = await service2.get_messages_for_conversation(
            conversation_id=conv2.id,
            user_id=user_id
        )
        assert len(messages2) == 1
        assert messages2[0].content == "Hello, second conversation!"


@pytest.mark.asyncio
async def test_message_persistence_across_sessions():
    """
    Test message persistence across sessions:
    Given a user is engaged in a conversation with the AI chatbot,
    When the user sends a new message,
    Then the message is stored in the conversation history with proper timestamp and role designation
    """
    engine = db_connection.engine
    async with AsyncSession(engine) as session1:
        service1 = ConversationService(session1)

        user_id = "test_user_messages"

        # Create a conversation
        conversation = await service1.create_conversation(user_id=user_id, title="Message Persistence Test")

        # Add a message
        message1 = await service1.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="First message in session 1"
        )

        # Verify the message was created
        assert message1.content == "First message in session 1"
        assert message1.role == "user"
        assert message1.conversation_id == conversation.id

        # Commit and close first session
        await session1.commit()

    # New session: Verify the message persists and add another
    async with AsyncSession(engine) as session2:
        service2 = ConversationService(session2)

        # Verify the first message still exists
        messages, total = await service2.get_messages_for_conversation(
            conversation_id=conversation.id,
            user_id=user_id
        )
        assert len(messages) == 1
        assert messages[0].content == "First message in session 1"

        # Add a second message in the new session
        message2 = await service2.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content="Response in session 2"
        )

        # Verify both messages exist
        messages, total = await service2.get_messages_for_conversation(
            conversation_id=conversation.id,
            user_id=user_id
        )
        assert len(messages) == 2
        assert messages[0].content == "First message in session 1"
        assert messages[1].content == "Response in session 2"
        assert messages[0].role == "user"
        assert messages[1].role == "assistant"

        # Verify messages are in chronological order
        assert messages[0].created_at <= messages[1].created_at


@pytest.mark.asyncio
async def test_conversation_metadata_persistence():
    """Test that conversation metadata is properly persisted"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session1:
        service1 = ConversationService(session1)

        user_id = "test_user_metadata"

        # Create a conversation with a title
        conversation = await service1.create_conversation(
            user_id=user_id,
            title="Metadata Persistence Test"
        )

        # Add a message to update the updated_at timestamp
        await service1.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="Test message"
        )

        original_updated_at = conversation.updated_at

        # Commit and close first session
        await session1.commit()

    # New session: Verify metadata persists
    async with AsyncSession(engine) as session2:
        service2 = ConversationService(session2)

        # Retrieve the conversation
        retrieved_conversation = await service2.get_conversation_by_id(
            conversation_id=conversation.id,
            user_id=user_id
        )

        # Verify all metadata is preserved
        assert retrieved_conversation.id == conversation.id
        assert retrieved_conversation.user_id == user_id
        assert retrieved_conversation.title == "Metadata Persistence Test"
        assert retrieved_conversation.created_at == conversation.created_at
        assert retrieved_conversation.updated_at >= original_updated_at


if __name__ == "__main__":
    # For running tests individually during development
    pass