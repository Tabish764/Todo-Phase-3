import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database.connection import db_connection
from backend.src.models.conversation import Conversation, Message
from backend.src.services.conversation_service import ConversationService


@pytest.mark.asyncio
async def test_conversation_context_access_patterns():
    """
    Test conversation context access patterns:
    Given a user has discussed specific todo items in a conversation,
    When the user refers to those items later using pronouns or partial descriptions,
    Then the AI system can access the conversation history to understand the context
    """
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "test_user_context_access"

        # Create a conversation about todos
        conversation = await service.create_conversation(user_id=user_id, title="Todo Planning Session")

        # Add messages discussing specific todo items
        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="I need to buy groceries including milk, bread, and eggs"
        )

        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content="Okay, I've added those grocery items to your list. When would you like to shop?"
        )

        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="Also need to schedule a doctor appointment and call mom"
        )

        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content="Got it. So your tasks are: buy groceries, schedule doctor appointment, and call mom."
        )

        # Now simulate the user referring back to previous items using pronouns
        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="What were the grocery items again?"
        )

        # Test that we can retrieve the context (recent messages) to understand what "the grocery items" refers to
        context_messages = await service.get_conversation_context(
            conversation_id=conversation.id,
            user_id=user_id,
            limit=5  # Get last 5 messages
        )

        assert len(context_messages) >= 3  # Should have at least the last few messages
        # Verify that the context includes the grocery discussion
        grocery_related_messages = [
            msg for msg in context_messages
            if "grocer" in msg.content.lower() or "milk" in msg.content.lower() or "bread" in msg.content.lower()
        ]
        assert len(grocery_related_messages) > 0  # Should find grocery-related context

        # Add another message where user refers to "those tasks"
        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="Can you remind me of those tasks?"
        )

        # Test context retrieval again
        context_messages = await service.get_conversation_context(
            conversation_id=conversation.id,
            user_id=user_id,
            limit=10  # Get last 10 messages
        )

        # Should include context about the tasks mentioned earlier
        task_related_messages = [
            msg for msg in context_messages
            if "task" in msg.content.lower() or "grocer" in msg.content.lower()
            or "doctor" in msg.content.lower() or "call mom" in msg.content.lower()
        ]
        assert len(task_related_messages) > 0


@pytest.mark.asyncio
async def test_multiple_conversation_context_isolation():
    """
    Test that context access is properly isolated between conversations:
    Given multiple conversations exist for a user,
    When the AI needs to access conversation context,
    Then it can efficiently retrieve the relevant conversation based on the current session
    """
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "test_user_multi_context"

        # Create first conversation about groceries
        grocery_conv = await service.create_conversation(user_id=user_id, title="Grocery Planning")

        await service.add_message_to_conversation(
            conversation_id=grocery_conv.id,
            user_id=user_id,
            role="user",
            content="Need to buy milk, eggs, and bread"
        )

        await service.add_message_to_conversation(
            conversation_id=grocery_conv.id,
            user_id=user_id,
            role="assistant",
            content="Added to your grocery list."
        )

        # Create second conversation about work tasks
        work_conv = await service.create_conversation(user_id=user_id, title="Work Tasks")

        await service.add_message_to_conversation(
            conversation_id=work_conv.id,
            user_id=user_id,
            role="user",
            content="Need to finish the report and schedule team meeting"
        )

        await service.add_message_to_conversation(
            conversation_id=work_conv.id,
            user_id=user_id,
            role="assistant",
            content="Noted. I'll help you prioritize these work tasks."
        )

        # Test context retrieval from grocery conversation
        grocery_context = await service.get_conversation_context(
            conversation_id=grocery_conv.id,
            user_id=user_id,
            limit=5
        )

        # Should only contain grocery-related messages
        assert len(grocery_context) > 0
        for msg in grocery_context:
            assert "grocer" in msg.content.lower() or "milk" in msg.content.lower() or \
                   "eggs" in msg.content.lower() or "bread" in msg.content.lower()

        # Test context retrieval from work conversation
        work_context = await service.get_conversation_context(
            conversation_id=work_conv.id,
            user_id=user_id,
            limit=5
        )

        # Should only contain work-related messages
        assert len(work_context) > 0
        for msg in work_context:
            assert "report" in msg.content.lower() or "meeting" in msg.content.lower() or \
                   "work" in msg.content.lower() or "task" in msg.content.lower()

        # Verify no cross-contamination between contexts
        grocery_content = " ".join([msg.content for msg in grocery_context]).lower()
        work_content = " ".join([msg.content for msg in work_context]).lower()

        # Grocery context should not contain work-specific terms (beyond general ones)
        assert not any(term in grocery_content for term in ["report", "meeting", "team"])
        # Work context should not contain grocery-specific terms (beyond general ones)
        assert not any(term in work_content for term in ["milk", "eggs", "bread"])


@pytest.mark.asyncio
async def test_context_retrieval_with_search():
    """Test that context can be retrieved using search functionality"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "test_user_search_context"

        # Create a conversation with various types of messages
        conversation = await service.create_conversation(user_id=user_id, title="Mixed Conversation")

        # Add messages with different roles
        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="I'm having trouble with my computer"
        )

        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content="I can help with that. What specific issue are you experiencing?"
        )

        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="The screen is flickering and it's running slow"
        )

        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="system",
            content="Diagnostic information: CPU usage high"
        )

        # Test searching for user messages
        user_messages, total = await service.search_messages_in_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            limit=10
        )

        assert len(user_messages) == 2  # Should find 2 user messages
        for msg in user_messages:
            assert msg.role == "user"

        # Test searching for specific content
        computer_messages, total = await service.search_messages_in_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            search_term="computer",
            limit=10
        )

        assert len(computer_messages) >= 1  # Should find at least one message about computer
        for msg in computer_messages:
            assert "computer" in msg.content.lower()

        # Test searching with both filters
        user_computer_messages, total = await service.search_messages_in_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            search_term="computer",
            role="user",
            limit=10
        )

        assert len(user_computer_messages) >= 1  # Should find user messages about computer
        for msg in user_computer_messages:
            assert msg.role == "user" and "computer" in msg.content.lower()


@pytest.mark.asyncio
async def test_context_ordering():
    """Test that context messages are properly ordered"""
    engine = db_connection.engine
    async with AsyncSession(engine) as session:
        service = ConversationService(session)

        user_id = "test_user_context_order"

        # Create a conversation
        conversation = await service.create_conversation(user_id=user_id, title="Ordering Test")

        # Add messages in chronological order
        msg1 = await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="First message"
        )

        msg2 = await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content="Second message"
        )

        msg3 = await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="Third message"
        )

        # Test chronological context (oldest first)
        context_messages = await service.get_conversation_context(
            conversation_id=conversation.id,
            user_id=user_id,
            limit=10
        )

        # Should return messages in chronological order (oldest first)
        assert len(context_messages) == 3
        assert context_messages[0].content == "First message"
        assert context_messages[1].content == "Second message"
        assert context_messages[2].content == "Third message"

        # Verify the ordering matches creation order
        assert context_messages[0].created_at <= context_messages[1].created_at <= context_messages[2].created_at


if __name__ == "__main__":
    # For running tests individually during development
    pass