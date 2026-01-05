import pytest
import time
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database.connection import db_connection
from backend.src.models.conversation import Conversation, Message
from backend.src.services.conversation_service import ConversationService


@pytest.mark.asyncio
async def test_conversation_context_retrieval_performance():
    """Test performance of conversation context retrieval - should be under 500ms for reasonable loads"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "test_user_performance"

        # Create a conversation
        conversation = await service.create_conversation(user_id=user_id, title="Performance Test Conversation")

        # Add multiple messages to the conversation (simulating a conversation with history)
        for i in range(50):
            await service.add_message_to_conversation(
                conversation_id=conversation.id,
                user_id=user_id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i}: This is a test message for performance evaluation."
            )

        # Measure time to retrieve conversation context (recent messages)
        start_time = time.time()

        messages = await service.get_conversation_context(
            conversation_id=conversation.id,
            user_id=user_id,
            limit=10  # Get last 10 messages
        )

        end_time = time.time()
        retrieval_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Verify the results
        assert len(messages) <= 10  # Should get at most 10 messages
        assert retrieval_time < 500  # Should be under 500ms (much faster in practice)
        print(f"Context retrieval time: {retrieval_time:.2f}ms for 10 recent messages from 50-message conversation")


@pytest.mark.asyncio
async def test_conversation_search_performance():
    """Test performance of conversation search functionality"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "test_user_search_performance"

        # Create a conversation
        conversation = await service.create_conversation(user_id=user_id, title="Search Performance Test")

        # Add multiple messages with various content
        for i in range(100):
            role = "user" if i % 3 == 0 else ("assistant" if i % 3 == 1 else "system")
            content = f"This is message number {i} with some searchable content. The quick brown fox jumps over the lazy dog."
            if i % 10 == 0:
                content += " SPECIAL_SEARCH_TERM "  # Add a term we can search for

            await service.add_message_to_conversation(
                conversation_id=conversation.id,
                user_id=user_id,
                role=role,
                content=content
            )

        # Measure time to search for messages
        start_time = time.time()

        messages, total = await service.search_messages_in_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            search_term="SPECIAL_SEARCH_TERM",
            limit=20
        )

        end_time = time.time()
        search_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Verify the results
        assert total > 0  # Should find some messages with the special term
        assert search_time < 1000  # Should be under 1 second (much faster with proper indexing)
        print(f"Search time: {search_time:.2f}ms for '{'SPECIAL_SEARCH_TERM'}' in 100-message conversation")


@pytest.mark.asyncio
async def test_multiple_conversations_performance():
    """Test performance when retrieving context from multiple conversations"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "test_user_multiple_conv"

        # Create multiple conversations
        conversations = []
        for i in range(10):
            conv = await service.create_conversation(user_id=user_id, title=f"Conversation {i}")
            conversations.append(conv)

            # Add a few messages to each conversation
            for j in range(5):
                await service.add_message_to_conversation(
                    conversation_id=conv.id,
                    user_id=user_id,
                    role="user",
                    content=f"Message {j} in conversation {i}"
                )

        # Measure time to get all user conversations
        start_time = time.time()

        user_conversations, total = await service.get_user_conversations(
            user_id=user_id,
            limit=20
        )

        end_time = time.time()
        retrieval_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Verify the results
        assert len(user_conversations) == 10  # Should get all 10 conversations
        assert total == 10
        assert retrieval_time < 500  # Should be under 500ms
        print(f"Multiple conversations retrieval time: {retrieval_time:.2f}ms for {len(user_conversations)} conversations")


@pytest.mark.asyncio
async def test_message_retrieval_performance():
    """Test performance of retrieving all messages from a conversation"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "test_user_msg_performance"

        # Create a conversation
        conversation = await service.create_conversation(user_id=user_id, title="Message Retrieval Performance Test")

        # Add many messages to the conversation
        num_messages = 200
        for i in range(num_messages):
            await service.add_message_to_conversation(
                conversation_id=conversation.id,
                user_id=user_id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Performance test message number {i} with some content to make it realistic."
            )

        # Measure time to retrieve all messages
        start_time = time.time()

        messages, total = await service.get_messages_for_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            limit=200
        )

        end_time = time.time()
        retrieval_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Verify the results
        assert len(messages) == num_messages  # Should get all messages
        assert total == num_messages
        assert retrieval_time < 1000  # Should be under 1 second (with proper indexing)
        print(f"Message retrieval time: {retrieval_time:.2f}ms for {len(messages)} messages")


if __name__ == "__main__":
    # For running tests individually during development
    pass