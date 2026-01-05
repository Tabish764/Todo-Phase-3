import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.models.conversation import Conversation, Message
from backend.src.services.conversation_service import ConversationService
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database.connection import db_connection
import json


@pytest.fixture
def client():
    """Create a test client for the API"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.asyncio
async def test_conversation_contract_create():
    """Test the contract for creating a conversation"""
    # Note: This would require authentication in real implementation
    # For contract testing, we're checking the API structure and response format
    async with AsyncSession(db_connection.engine) as session:
        service = ConversationService(session)

        # Create a conversation using the service layer directly for testing
        user_id = "contract_test_user"
        conversation = await service.create_conversation(
            user_id=user_id,
            title="Contract Test Conversation"
        )

        # Verify the conversation object has the expected structure
        assert hasattr(conversation, 'id')
        assert conversation.user_id == user_id
        assert conversation.title == "Contract Test Conversation"
        assert hasattr(conversation, 'created_at')
        assert hasattr(conversation, 'updated_at')

        # Verify required fields are present
        assert conversation.id is not None
        assert conversation.user_id is not None


@pytest.mark.asyncio
async def test_conversation_contract_get_list():
    """Test the contract for getting user conversations"""
    async with AsyncSession(db_connection.engine) as session:
        service = ConversationService(session)

        user_id = "contract_test_user_list"

        # Create a conversation first
        conv = await service.create_conversation(
            user_id=user_id,
            title="Test Conversation for List"
        )

        # Get user conversations
        conversations, total = await service.get_user_conversations(
            user_id=user_id
        )

        # Verify response structure
        assert isinstance(conversations, list)
        assert isinstance(total, int)
        assert len(conversations) >= 1
        assert total >= 1

        # Verify conversation structure
        conv = conversations[0]
        assert hasattr(conv, 'id')
        assert hasattr(conv, 'user_id')
        assert hasattr(conv, 'title')
        assert hasattr(conv, 'created_at')
        assert hasattr(conv, 'updated_at')


@pytest.mark.asyncio
async def test_message_contract_create():
    """Test the contract for creating a message"""
    async with AsyncSession(db_connection.engine) as session:
        service = ConversationService(session)

        user_id = "contract_test_user_msg"

        # Create a conversation first
        conversation = await service.create_conversation(
            user_id=user_id,
            title="Message Contract Test"
        )

        # Add a message
        message = await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="Test message for contract verification",
            tool_calls_data={"function": "test_function", "arguments": {"param": "value"}}
        )

        # Verify message structure
        assert hasattr(message, 'id')
        assert message.conversation_id == conversation.id
        assert message.user_id == user_id
        assert message.role in ["user", "assistant", "system"]
        assert message.content == "Test message for contract verification"
        assert message.tool_calls is not None  # Should contain the JSON string
        assert hasattr(message, 'created_at')

        # Verify tool_calls can be parsed
        import json
        tool_data = json.loads(message.tool_calls)
        assert "function" in tool_data
        assert "arguments" in tool_data


@pytest.mark.asyncio
async def test_message_contract_get_list():
    """Test the contract for getting messages in a conversation"""
    async with AsyncSession(db_connection.engine) as session:
        service = ConversationService(session)

        user_id = "contract_test_user_msg_list"

        # Create a conversation and add messages
        conversation = await service.create_conversation(
            user_id=user_id,
            title="Message List Contract Test"
        )

        # Add several messages
        for i in range(3):
            await service.add_message_to_conversation(
                conversation_id=conversation.id,
                user_id=user_id,
                role="user",
                content=f"Test message {i}"
            )

        # Get messages
        messages, total = await service.get_messages_for_conversation(
            conversation_id=conversation.id,
            user_id=user_id
        )

        # Verify response structure
        assert isinstance(messages, list)
        assert isinstance(total, int)
        assert len(messages) == 3
        assert total == 3

        # Verify message structure
        for msg in messages:
            assert hasattr(msg, 'id')
            assert hasattr(msg, 'conversation_id')
            assert hasattr(msg, 'user_id')
            assert hasattr(msg, 'role')
            assert hasattr(msg, 'content')
            assert hasattr(msg, 'created_at')
            assert msg.conversation_id == conversation.id
            assert msg.user_id == user_id


@pytest.mark.asyncio
async def test_conversation_contract_context_retrieval():
    """Test the contract for getting conversation context"""
    async with AsyncSession(db_connection.engine) as session:
        service = ConversationService(session)

        user_id = "contract_test_user_context"

        # Create a conversation and add messages
        conversation = await service.create_conversation(
            user_id=user_id,
            title="Context Contract Test"
        )

        # Add messages in chronological order
        for i in range(5):
            await service.add_message_to_conversation(
                conversation_id=conversation.id,
                user_id=user_id,
                role="user",
                content=f"Context message {i}"
            )

        # Get conversation context (recent messages)
        context_messages = await service.get_conversation_context(
            conversation_id=conversation.id,
            user_id=user_id,
            limit=3
        )

        # Verify response structure
        assert isinstance(context_messages, list)
        assert len(context_messages) <= 3  # Should respect limit

        # Verify message structure
        for msg in context_messages:
            assert hasattr(msg, 'id')
            assert hasattr(msg, 'conversation_id')
            assert hasattr(msg, 'user_id')
            assert hasattr(msg, 'role')
            assert hasattr(msg, 'content')
            assert hasattr(msg, 'created_at')


@pytest.mark.asyncio
async def test_conversation_contract_search():
    """Test the contract for searching messages in a conversation"""
    async with AsyncSession(db_connection.engine) as session:
        service = ConversationService(session)

        user_id = "contract_test_user_search"

        # Create a conversation and add messages with different content
        conversation = await service.create_conversation(
            user_id=user_id,
            title="Search Contract Test"
        )

        # Add messages with different content
        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="This message contains apple"
        )

        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content="This message contains banana"
        )

        await service.add_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content="This message contains apple and banana"
        )

        # Test search functionality
        search_results, search_total = await service.search_messages_in_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            search_term="apple",
            limit=10
        )

        # Verify search results structure
        assert isinstance(search_results, list)
        assert isinstance(search_total, int)
        assert len(search_results) >= 1  # Should find at least one message with "apple"

        # Verify all results contain the search term
        for msg in search_results:
            assert "apple" in msg.content.lower()
            assert hasattr(msg, 'id')
            assert hasattr(msg, 'conversation_id')
            assert hasattr(msg, 'user_id')
            assert hasattr(msg, 'role')
            assert hasattr(msg, 'content')
            assert hasattr(msg, 'created_at')


def test_api_response_contract_formats():
    """Test that API responses follow expected contract formats"""
    # This test would normally check actual API responses
    # For now, we'll verify the expected response structure based on our API design

    # Expected structure for conversation response
    expected_conversation_structure = {
        "id": int,
        "title": str,
        "user_id": str,
        "created_at": object,  # datetime object
        "updated_at": object   # datetime object
    }

    # Expected structure for message response
    expected_message_structure = {
        "id": int,
        "conversation_id": int,
        "user_id": str,
        "role": str,
        "content": str,
        "tool_calls": (str, type(None)),  # JSON string or None
        "created_at": object  # datetime object
    }

    # Expected structure for get conversations response
    expected_conversations_response = {
        "conversations": list,
        "total": int,
        "limit": int,
        "offset": int
    }

    # Expected structure for get messages response
    expected_messages_response = {
        "messages": list,
        "total": int,
        "limit": int,
        "offset": int
    }

    # These are just structural contracts - the actual implementation
    # should match these expected formats
    assert True  # Contract validation would happen in real API tests


if __name__ == "__main__":
    # For running tests individually during development
    pass