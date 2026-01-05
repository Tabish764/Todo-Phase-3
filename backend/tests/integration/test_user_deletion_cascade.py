import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database.connection import db_connection
from backend.src.models.conversation import Conversation, Message
from backend.src.services.conversation_service import ConversationService


@pytest.mark.asyncio
async def test_user_account_deletion_cascade():
    """
    Test user account deletion and cascade effects:
    Given a user account is deleted,
    When the system processes the deletion,
    Then all associated conversations and messages are also removed
    """
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "user_for_deletion_test"

        # Create conversations for the user
        conv1 = await service.create_conversation(user_id=user_id, title="First Conversation for Deletion")
        conv2 = await service.create_conversation(user_id=user_id, title="Second Conversation for Deletion")
        conv3 = await service.create_conversation(user_id=user_id, title="Third Conversation for Deletion")

        # Add multiple messages to each conversation
        # Add 5 messages to first conversation
        for i in range(5):
            await service.add_message_to_conversation(
                conversation_id=conv1.id,
                user_id=user_id,
                role="user",
                content=f"Message {i} in first conversation"
            )

        # Add 3 messages to second conversation
        for i in range(3):
            await service.add_message_to_conversation(
                conversation_id=conv2.id,
                user_id=user_id,
                role="assistant",
                content=f"Message {i} in second conversation"
            )

        # Add 7 messages to third conversation
        for i in range(7):
            await service.add_message_to_conversation(
                conversation_id=conv3.id,
                user_id=user_id,
                role="user",
                content=f"Message {i} in third conversation"
            )

        # Verify all conversations and messages exist before deletion
        user_conversations, total_convs_before = await service.get_user_conversations(user_id=user_id)
        assert len(user_conversations) == 3
        assert total_convs_before == 3

        # Count total messages across all conversations before deletion
        total_messages_before = 0
        for conv in user_conversations:
            _, msg_count = await service.get_messages_for_conversation(
                conversation_id=conv.id,
                user_id=user_id
            )
            total_messages_before += msg_count

        assert total_messages_before == 15  # 5 + 3 + 7 = 15 messages

        # Perform the deletion
        deleted_count = await service.delete_conversations_for_user(user_id=user_id)

        assert deleted_count == 3  # Should have deleted 3 conversations

        # Verify that all conversations are gone
        user_conversations_after, total_after = await service.get_user_conversations(user_id=user_id)
        assert len(user_conversations_after) == 0
        assert total_after == 0

        # Verify that no messages remain for this user's conversations
        # (This depends on the cascade delete working properly in the database)
        # We'll test this by trying to access any conversation data for the user
        for conv in [conv1, conv2, conv3]:
            try:
                # Try to get messages from the deleted conversation
                messages, _ = await service.get_messages_for_conversation(
                    conversation_id=conv.id,
                    user_id=user_id
                )
                # If we get here, the conversation still exists somehow
                assert False, f"Conversation {conv.id} should have been deleted"
            except ValueError:
                # Expected - conversation no longer exists
                pass

        # Verify that the conversations no longer exist when accessed directly
        for conv in [conv1, conv2, conv3]:
            retrieved_conv = await service.get_conversation_by_id(
                conversation_id=conv.id,
                user_id=user_id
            )
            assert retrieved_conv is None


@pytest.mark.asyncio
async def test_user_deletion_with_context_access():
    """Test that after user deletion, context access is no longer possible"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "user_context_deletion_test"

        # Create a conversation with some history
        conversation = await service.create_conversation(user_id=user_id, title="Conversation for Context Test")

        # Add messages to build context
        for i in range(10):
            await service.add_message_to_conversation(
                conversation_id=conversation.id,
                user_id=user_id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Context message {i} for deletion test"
            )

        # Verify context is accessible before deletion
        context_before = await service.get_conversation_context(
            conversation_id=conversation.id,
            user_id=user_id,
            limit=5
        )
        assert len(context_before) == 5  # Should get 5 most recent messages

        # Perform deletion
        deleted_count = await service.delete_conversations_for_user(user_id=user_id)
        assert deleted_count == 1

        # Verify context is no longer accessible after deletion
        try:
            context_after = await service.get_conversation_context(
                conversation_id=conversation.id,
                user_id=user_id,
                limit=5
            )
            # Should not reach here
            assert False, "Context should not be accessible after deletion"
        except ValueError:
            # Expected - conversation no longer exists
            pass


@pytest.mark.asyncio
async def test_user_deletion_selective_impact():
    """Test that deleting one user doesn't affect other users' data"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        # Create multiple users
        user_to_delete = "user_to_delete"
        user_to_keep1 = "user_to_keep_1"
        user_to_keep2 = "user_to_keep_2"

        # Create conversations for all users
        conv_delete = await service.create_conversation(user_id=user_to_delete, title="To be deleted")
        conv_keep1 = await service.create_conversation(user_id=user_to_keep1, title="User 1 - keep")
        conv_keep2 = await service.create_conversation(user_id=user_to_keep2, title="User 2 - keep")

        # Add messages for each user
        for i in range(5):
            await service.add_message_to_conversation(
                conversation_id=conv_delete.id,
                user_id=user_to_delete,
                role="user",
                content=f"Message {i} for deletion"
            )
            await service.add_message_to_conversation(
                conversation_id=conv_keep1.id,
                user_id=user_to_keep1,
                role="user",
                content=f"Message {i} for user 1"
            )
            await service.add_message_to_conversation(
                conversation_id=conv_keep2.id,
                user_id=user_to_keep2,
                role="user",
                content=f"Message {i} for user 2"
            )

        # Verify all users have their data before deletion
        delete_convs, delete_total = await service.get_user_conversations(user_id=user_to_delete)
        keep1_convs, keep1_total = await service.get_user_conversations(user_id=user_to_keep1)
        keep2_convs, keep2_total = await service.get_user_conversations(user_id=user_to_keep2)

        assert len(delete_convs) == 1 and delete_total == 1
        assert len(keep1_convs) == 1 and keep1_total == 1
        assert len(keep2_convs) == 1 and keep2_total == 1

        # Delete only one user
        deleted_count = await service.delete_conversations_for_user(user_id=user_to_delete)
        assert deleted_count == 1

        # Verify that deleted user's data is gone
        delete_convs_after, delete_total_after = await service.get_user_conversations(user_id=user_to_delete)
        assert len(delete_convs_after) == 0 and delete_total_after == 0

        # Verify that other users' data remains intact
        keep1_convs_after, keep1_total_after = await service.get_user_conversations(user_id=user_to_keep1)
        keep2_convs_after, keep2_total_after = await service.get_user_conversations(user_id=user_to_keep2)

        assert len(keep1_convs_after) == 1 and keep1_total_after == 1
        assert len(keep2_convs_after) == 1 and keep2_total_after == 1

        # Verify other users can still access their conversations
        conv1_check = await service.get_conversation_by_id(
            conversation_id=conv_keep1.id,
            user_id=user_to_keep1
        )
        conv2_check = await service.get_conversation_by_id(
            conversation_id=conv_keep2.id,
            user_id=user_to_keep2
        )

        assert conv1_check is not None
        assert conv2_check is not None

        # Verify other users can still access their messages
        msgs1, total1 = await service.get_messages_for_conversation(
            conversation_id=conv_keep1.id,
            user_id=user_to_keep1
        )
        msgs2, total2 = await service.get_messages_for_conversation(
            conversation_id=conv_keep2.id,
            user_id=user_to_keep2
        )

        assert len(msgs1) == 5 and total1 == 5
        assert len(msgs2) == 5 and total2 == 5


@pytest.mark.asyncio
async def test_empty_user_deletion():
    """Test deleting a user that has no conversations"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_no_convs = "user_with_no_conversations"

        # Verify user has no conversations initially
        user_convs, user_total = await service.get_user_conversations(user_id=user_no_convs)
        assert len(user_convs) == 0
        assert user_total == 0

        # Try to delete conversations for user with no conversations
        deleted_count = await service.delete_conversations_for_user(user_id=user_no_convs)

        # Should return 0 (no conversations to delete)
        assert deleted_count == 0

        # Verify user still has no conversations after "deletion"
        user_convs_after, user_total_after = await service.get_user_conversations(user_id=user_no_convs)
        assert len(user_convs_after) == 0
        assert user_total_after == 0


if __name__ == "__main__":
    # For running tests individually during development
    pass