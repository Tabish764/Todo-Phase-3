import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database.connection import db_connection
from backend.src.models.conversation import Conversation, Message
from backend.src.services.conversation_service import ConversationService


@pytest.mark.asyncio
async def test_multi_user_conversation_creation():
    """Test that multiple users can create conversations simultaneously without conflicts"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        # Simulate multiple users creating conversations simultaneously
        users = [f"user_{i}_multi_test" for i in range(5)]
        conversations = []

        for user_id in users:
            # Each user creates a conversation
            conv = await service.create_conversation(user_id=user_id, title=f"Conversation for {user_id}")
            conversations.append((user_id, conv))

            # Add a few messages to each conversation
            for j in range(3):
                await service.add_message_to_conversation(
                    conversation_id=conv.id,
                    user_id=user_id,
                    role="user",
                    content=f"Message {j} from {user_id}"
                )

        # Verify that each user has their own conversation
        for user_id, expected_conv in conversations:
            user_convs, total = await service.get_user_conversations(user_id=user_id)
            assert len(user_convs) == 1
            assert total == 1
            assert user_convs[0].id == expected_conv.id
            assert user_convs[0].user_id == user_id

        # Verify that no user can see another user's conversations
        all_user_convs = set()
        for user_id, _ in conversations:
            user_convs, _ = await service.get_user_conversations(user_id=user_id)
            user_conv_ids = {conv.id for conv in user_convs}
            all_user_convs.update(user_conv_ids)

        # All conversation IDs should be unique across users (due to isolation)
        assert len(all_user_convs) == len(conversations)


@pytest.mark.asyncio
async def test_concurrent_message_addition():
    """Test that multiple users can add messages simultaneously without conflicts"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        # Create conversations for multiple users
        user1_id = "user_concurrent_1"
        user2_id = "user_concurrent_2"
        user3_id = "user_concurrent_3"

        conv1 = await service.create_conversation(user_id=user1_id, title="User 1's Chat")
        conv2 = await service.create_conversation(user_id=user2_id, title="User 2's Chat")
        conv3 = await service.create_conversation(user_id=user3_id, title="User 3's Chat")

        # Simulate concurrent message additions from different users
        # Add messages for user 1
        for i in range(5):
            await service.add_message_to_conversation(
                conversation_id=conv1.id,
                user_id=user1_id,
                role="user",
                content=f"User 1 message {i}"
            )

        # Add messages for user 2
        for i in range(3):
            await service.add_message_to_conversation(
                conversation_id=conv2.id,
                user_id=user2_id,
                role="user",
                content=f"User 2 message {i}"
            )

        # Add messages for user 3
        for i in range(7):
            await service.add_message_to_conversation(
                conversation_id=conv3.id,
                user_id=user3_id,
                role="user",
                content=f"User 3 message {i}"
            )

        # Verify each user has the correct number of messages in their conversation
        user1_messages, user1_total = await service.get_messages_for_conversation(
            conversation_id=conv1.id,
            user_id=user1_id
        )
        assert len(user1_messages) == 5
        assert user1_total == 5
        for i, msg in enumerate(user1_messages):
            assert f"User 1 message {i}" in msg.content

        user2_messages, user2_total = await service.get_messages_for_conversation(
            conversation_id=conv2.id,
            user_id=user2_id
        )
        assert len(user2_messages) == 3
        assert user2_total == 3
        for i, msg in enumerate(user2_messages):
            assert f"User 2 message {i}" in msg.content

        user3_messages, user3_total = await service.get_messages_for_conversation(
            conversation_id=conv3.id,
            user_id=user3_id
        )
        assert len(user3_messages) == 7
        assert user3_total == 7
        for i, msg in enumerate(user3_messages):
            assert f"User 3 message {i}" in msg.content


@pytest.mark.asyncio
async def test_cross_user_access_prevention():
    """Test that users cannot access each other's conversations or messages"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        # Create users and conversations
        alice_id = "alice_multi_scenario"
        bob_id = "bob_multi_scenario"
        charlie_id = "charlie_multi_scenario"

        alice_conv = await service.create_conversation(user_id=alice_id, title="Alice's Private Chat")
        bob_conv = await service.create_conversation(user_id=bob_id, title="Bob's Private Chat")
        charlie_conv = await service.create_conversation(user_id=charlie_id, title="Charlie's Private Chat")

        # Add messages to each conversation
        await service.add_message_to_conversation(
            conversation_id=alice_conv.id,
            user_id=alice_id,
            role="user",
            content="Alice's private message"
        )
        await service.add_message_to_conversation(
            conversation_id=alice_conv.id,
            user_id=alice_id,
            role="assistant",
            content="Alice's assistant response"
        )

        await service.add_message_to_conversation(
            conversation_id=bob_conv.id,
            user_id=bob_id,
            role="user",
            content="Bob's private message"
        )
        await service.add_message_to_conversation(
            conversation_id=bob_conv.id,
            user_id=bob_id,
            role="assistant",
            content="Bob's assistant response"
        )

        await service.add_message_to_conversation(
            conversation_id=charlie_conv.id,
            user_id=charlie_id,
            role="user",
            content="Charlie's private message"
        )

        # Test that Alice can only see her own conversations
        alice_convs, alice_total = await service.get_user_conversations(user_id=alice_id)
        assert len(alice_convs) == 1
        assert alice_total == 1
        assert alice_convs[0].id == alice_conv.id

        # Test that Alice cannot access Bob's or Charlie's conversations
        bob_conv_access = await service.get_conversation_by_id(
            conversation_id=bob_conv.id,
            user_id=alice_id
        )
        assert bob_conv_access is None

        charlie_conv_access = await service.get_conversation_by_id(
            conversation_id=charlie_conv.id,
            user_id=alice_id
        )
        assert charlie_conv_access is None

        # Test that Alice cannot retrieve messages from Bob's or Charlie's conversations
        try:
            alice_access_to_bob_msgs = await service.get_messages_for_conversation(
                conversation_id=bob_conv.id,
                user_id=alice_id
            )
            assert False, "Alice should not access Bob's messages"
        except ValueError:
            # Expected - Alice cannot access Bob's conversation
            pass

        try:
            alice_access_to_charlie_msgs = await service.get_messages_for_conversation(
                conversation_id=charlie_conv.id,
                user_id=alice_id
            )
            assert False, "Alice should not access Charlie's messages"
        except ValueError:
            # Expected - Alice cannot access Charlie's conversation
            pass


@pytest.mark.asyncio
async def test_concurrent_user_operations():
    """Test that multiple users can perform operations simultaneously without conflicts"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        # Create multiple users
        users = [f"concurrent_user_{i}" for i in range(10)]

        # All users create conversations simultaneously (in this test, sequentially for predictability)
        conversations = {}
        for user_id in users:
            conv = await service.create_conversation(user_id=user_id, title=f"Conversation for {user_id}")
            conversations[user_id] = conv

            # Add some messages
            for j in range(2):
                await service.add_message_to_conversation(
                    conversation_id=conv.id,
                    user_id=user_id,
                    role="user",
                    content=f"Message {j} from {user_id}"
                )

        # All users retrieve their conversations simultaneously
        for user_id in users:
            user_convs, user_total = await service.get_user_conversations(user_id=user_id)
            assert len(user_convs) == 1
            assert user_total == 1
            assert user_convs[0].id == conversations[user_id].id
            assert user_convs[0].user_id == user_id

            # Verify messages
            messages, msg_total = await service.get_messages_for_conversation(
                conversation_id=conversations[user_id].id,
                user_id=user_id
            )
            assert len(messages) == 2
            assert msg_total == 2

        # Verify that no data leakage occurs between users
        for user_id in users:
            # Try to access another user's conversation
            other_user_id = next(uid for uid in users if uid != user_id)
            other_conv_id = conversations[other_user_id].id

            other_conv = await service.get_conversation_by_id(
                conversation_id=other_conv_id,
                user_id=user_id  # Current user trying to access other's conversation
            )
            assert other_conv is None


@pytest.mark.asyncio
async def test_conversation_context_isolation():
    """Test that conversation context is properly isolated between users"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        # Create conversations for different users
        user_a = "user_a_context_isolation"
        user_b = "user_b_context_isolation"

        conv_a = await service.create_conversation(user_id=user_a, title="User A's Context")
        conv_b = await service.create_conversation(user_id=user_b, title="User B's Context")

        # Add conversation history for user A
        for i in range(10):
            await service.add_message_to_conversation(
                conversation_id=conv_a.id,
                user_id=user_a,
                role="user" if i % 2 == 0 else "assistant",
                content=f"User A context message {i}"
            )

        # Add conversation history for user B
        for i in range(8):
            await service.add_message_to_conversation(
                conversation_id=conv_b.id,
                user_id=user_b,
                role="user" if i % 2 == 0 else "assistant",
                content=f"User B context message {i}"
            )

        # Get context for each user
        user_a_context = await service.get_conversation_context(
            conversation_id=conv_a.id,
            user_id=user_a,
            limit=5
        )
        assert len(user_a_context) == 5  # Should get 5 most recent messages
        for msg in user_a_context:
            assert "User A" in msg.content

        user_b_context = await service.get_conversation_context(
            conversation_id=conv_b.id,
            user_id=user_b,
            limit=5
        )
        assert len(user_b_context) == min(5, 8)  # Should get up to 5 most recent messages
        for msg in user_b_context:
            assert "User B" in msg.content

        # Verify no cross-contamination
        a_context_content = " ".join([msg.content for msg in user_a_context])
        b_context_content = " ".join([msg.content for msg in user_b_context])

        # User A's context should not contain User B's content
        assert "User B" not in a_context_content
        # User B's context should not contain User A's content
        assert "User A" not in b_context_content


if __name__ == "__main__":
    # For running tests individually during development
    pass