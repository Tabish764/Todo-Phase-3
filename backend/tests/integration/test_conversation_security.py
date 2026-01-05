import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database.connection import db_connection
from backend.src.models.conversation import Conversation, Message
from backend.src.services.conversation_service import ConversationService


@pytest.mark.asyncio
async def test_conversation_isolation_between_users():
    """
    Test that users can only access their own conversations:
    Given multiple users have conversations with the AI chatbot,
    When each user accesses their conversation history,
    Then they only see their own conversations and messages
    """
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        # Create two different users
        user1_id = "user_1_security_test"
        user2_id = "user_2_security_test"

        # Create conversations for user 1
        conv1_user1 = await service.create_conversation(user_id=user1_id, title="User 1's Conversation 1")
        conv2_user1 = await service.create_conversation(user_id=user1_id, title="User 1's Conversation 2")

        # Add messages to user 1's conversations
        await service.add_message_to_conversation(
            conversation_id=conv1_user1.id,
            user_id=user1_id,
            role="user",
            content="User 1 message 1"
        )
        await service.add_message_to_conversation(
            conversation_id=conv2_user1.id,
            user_id=user1_id,
            role="assistant",
            content="User 1 message 2"
        )

        # Create conversations for user 2
        conv1_user2 = await service.create_conversation(user_id=user2_id, title="User 2's Conversation 1")
        conv2_user2 = await service.create_conversation(user_id=user2_id, title="User 2's Conversation 2")

        # Add messages to user 2's conversations
        await service.add_message_to_conversation(
            conversation_id=conv1_user2.id,
            user_id=user2_id,
            role="user",
            content="User 2 message 1"
        )
        await service.add_message_to_conversation(
            conversation_id=conv2_user2.id,
            user_id=user2_id,
            role="assistant",
            content="User 2 message 2"
        )

        # Test that user 1 can only see their own conversations
        user1_conversations, user1_total = await service.get_user_conversations(user_id=user1_id)
        assert len(user1_conversations) == 2
        assert user1_total == 2
        user1_conv_ids = {conv.id for conv in user1_conversations}
        assert conv1_user1.id in user1_conv_ids
        assert conv2_user1.id in user1_conv_ids
        # User 1 should not see user 2's conversations
        assert conv1_user2.id not in user1_conv_ids
        assert conv2_user2.id not in user1_conv_ids

        # Test that user 2 can only see their own conversations
        user2_conversations, user2_total = await service.get_user_conversations(user_id=user2_id)
        assert len(user2_conversations) == 2
        assert user2_total == 2
        user2_conv_ids = {conv.id for conv in user2_conversations}
        assert conv1_user2.id in user2_conv_ids
        assert conv2_user2.id in user2_conv_ids
        # User 2 should not see user 1's conversations
        assert conv1_user1.id not in user2_conv_ids
        assert conv2_user1.id not in user2_conv_ids

        # Test that users cannot access each other's conversations directly
        user1_conv1_by_user2 = await service.get_conversation_by_id(
            conversation_id=conv1_user1.id,
            user_id=user2_id  # User 2 trying to access user 1's conversation
        )
        assert user1_conv1_by_user2 is None

        user2_conv1_by_user1 = await service.get_conversation_by_id(
            conversation_id=conv1_user2.id,
            user_id=user1_id  # User 1 trying to access user 2's conversation
        )
        assert user2_conv1_by_user1 is None

        # Test that users cannot access each other's messages
        try:
            user1_messages_from_user2_conv, _ = await service.get_messages_for_conversation(
                conversation_id=conv1_user1.id,
                user_id=user2_id  # User 2 trying to access user 1's messages
            )
            # This should raise an exception due to ownership validation
            assert False, "User 2 should not be able to access user 1's messages"
        except ValueError:
            # Expected - user 2 cannot access user 1's conversation
            pass

        try:
            user2_messages_from_user1_conv, _ = await service.get_messages_for_conversation(
                conversation_id=conv1_user2.id,
                user_id=user1_id  # User 1 trying to access user 2's messages
            )
            # This should raise an exception due to ownership validation
            assert False, "User 1 should not be able to access user 2's messages"
        except ValueError:
            # Expected - user 1 cannot access user 2's conversation
            pass


@pytest.mark.asyncio
async def test_message_isolation_between_users():
    """Test that users can only access their own messages within conversations"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        # Create a shared conversation ID concept (in reality, this wouldn't happen due to isolation,
        # but we're testing the access controls)
        user1_id = "user_1_msg_isolation"
        user2_id = "user_2_msg_isolation"

        # Each user creates their own conversation
        user1_conv = await service.create_conversation(user_id=user1_id, title="User 1's Private Chat")
        user2_conv = await service.create_conversation(user_id=user2_id, title="User 2's Private Chat")

        # Add messages to each conversation
        await service.add_message_to_conversation(
            conversation_id=user1_conv.id,
            user_id=user1_id,
            role="user",
            content="User 1's private message"
        )

        await service.add_message_to_conversation(
            conversation_id=user2_conv.id,
            user_id=user2_id,
            role="user",
            content="User 2's private message"
        )

        # Verify user isolation
        user1_msgs, user1_msg_count = await service.get_messages_for_conversation(
            conversation_id=user1_conv.id,
            user_id=user1_id
        )
        assert len(user1_msgs) == 1
        assert user1_msgs[0].content == "User 1's private message"

        user2_msgs, user2_msg_count = await service.get_messages_for_conversation(
            conversation_id=user2_conv.id,
            user_id=user2_id
        )
        assert len(user2_msgs) == 1
        assert user2_msgs[0].content == "User 2's private message"

        # Try to access the other user's conversation (should fail)
        try:
            other_msgs, _ = await service.get_messages_for_conversation(
                conversation_id=user1_conv.id,  # User 2 trying to access user 1's conversation
                user_id=user2_id
            )
            assert False, "User 2 should not access user 1's messages"
        except ValueError:
            pass  # Expected behavior


@pytest.mark.asyncio
async def test_conversation_search_isolation():
    """Test that conversation search is isolated by user"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user1_id = "user_1_search_isolation"
        user2_id = "user_2_search_isolation"

        # Create conversations for both users
        user1_conv = await service.create_conversation(user_id=user1_id, title="User 1's Search Test")
        user2_conv = await service.create_conversation(user_id=user2_id, title="User 2's Search Test")

        # Add messages with similar content but different users
        await service.add_message_to_conversation(
            conversation_id=user1_conv.id,
            user_id=user1_id,
            role="user",
            content="This is a private message for user 1 with secret content"
        )

        await service.add_message_to_conversation(
            conversation_id=user2_conv.id,
            user_id=user2_id,
            role="user",
            content="This is a private message for user 2 with secret content"
        )

        # User 1 searches for "secret" in their conversation
        user1_search_results, user1_search_total = await service.search_messages_in_conversation(
            conversation_id=user1_conv.id,
            user_id=user1_id,
            search_term="secret"
        )
        assert len(user1_search_results) == 1
        assert "user 1" in user1_search_results[0].content

        # User 2 searches for "secret" in their conversation
        user2_search_results, user2_search_total = await service.search_messages_in_conversation(
            conversation_id=user2_conv.id,
            user_id=user2_id,
            search_term="secret"
        )
        assert len(user2_search_results) == 1
        assert "user 2" in user2_search_results[0].content

        # Verify that search doesn't cross user boundaries
        # User 1 shouldn't find user 2's messages when searching in their own conversation
        # (This is tested by the conversation-specific search)


if __name__ == "__main__":
    # For running tests individually during development
    pass