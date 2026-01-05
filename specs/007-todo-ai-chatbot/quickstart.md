# Quickstart: Todo AI Chatbot - Database Schema for Conversations

## Overview
This guide helps you set up the database schema for conversations and messages to enable stateless operation of the Todo AI Chatbot.

## Prerequisites
- Python 3.12
- PostgreSQL database
- FastAPI application
- Existing user authentication system (Better Auth)

## Setup Steps

### 1. Install Dependencies
```bash
pip install sqlmodel sqlalchemy psycopg2-binary slowapi
```

### 2. Database Migration
Run the migration to create the conversations and messages tables:

```bash
# If using alembic
alembic revision --autogenerate -m "Add conversation tables"
alembic upgrade head

# Or run the migration directly
python -m backend.src.migrations.versions.007_add_conversation_tables
```

### 3. Verify Database Schema
After migration, verify that the tables exist with the correct structure:

```sql
-- Check conversations table
\d conversations;

-- Check messages table
\d messages;
```

### 4. Test the Models
Run the unit tests to ensure the models work correctly:

```bash
pytest tests/unit/test_conversation_models.py
```

### 5. Test the API
Test the conversation API endpoints:

```bash
# Create a conversation
curl -X POST http://localhost:8000/api/v1/conversations/ -H "Content-Type: application/json" -d '{"title": "My Todo Chat"}'

# Get user's conversations
curl -X GET http://localhost:8000/api/v1/conversations/

# Add a message to conversation
curl -X POST http://localhost:8000/api/v1/conversations/{conversation_id}/messages -H "Content-Type: application/json" -d '{"role": "user", "content": "Help me organize my tasks", "tool_calls": {"function": "get_user_todos", "arguments": {}}}'

# Get messages in a conversation
curl -X GET http://localhost:8000/api/v1/conversations/{conversation_id}/messages

# Get conversation context (recent messages)
curl -X GET http://localhost:8000/api/v1/conversations/{conversation_id}/context

# Search messages in conversation
curl -X GET "http://localhost:8000/api/v1/conversations/{conversation_id}/messages/search?search_term=todos&role=user"
```

## Key Components

### Models
- `Conversation`: Represents a chat session with metadata
- `Message`: Represents individual messages within conversations with role, content, and tool calls

### Services
- `ConversationService`: Handles business logic for conversations and messages
- Methods include: create_conversation, get_user_conversations, add_message, get_conversation_history, get_conversation_context, search_messages_in_conversation

### API Endpoints
- `POST /api/v1/conversations/`: Create a new conversation
- `GET /api/v1/conversations/`: Get user's conversations
- `GET /api/v1/conversations/{id}/`: Get specific conversation details
- `POST /api/v1/conversations/{id}/messages`: Add a message to conversation
- `GET /api/v1/conversations/{id}/messages`: Get messages in a conversation
- `GET /api/v1/conversations/{id}/context`: Get recent messages for AI context
- `GET /api/v1/conversations/{id}/messages/search`: Search messages with filters

### Rate Limiting
- Conversation creation: 5 requests per minute per IP
- Conversation listing: 30 requests per minute per IP
- Message creation: 20 requests per minute per IP
- Message listing: 30 requests per minute per IP
- Context retrieval: 30 requests per minute per IP
- Search: 15 requests per minute per IP

## Common Operations

### Creating a Conversation
```python
from backend.src.services.conversation_service import ConversationService

service = ConversationService(db_session)
conversation = await service.create_conversation(user_id="user123", title="Todo Planning Session")
```

### Adding a Message
```python
message = await service.add_message_to_conversation(
    conversation_id=conversation.id,
    user_id="user123",
    role="user",
    content="I need help organizing my tasks",
    tool_calls_data={"function": "get_user_todos", "arguments": {}}
)
```

### Retrieving Conversation History
```python
messages, total = await service.get_messages_for_conversation(
    conversation_id=conversation.id,
    user_id="user123",
    limit=50,
    offset=0
)
```

### Getting Conversation Context for AI
```python
context_messages = await service.get_conversation_context(
    conversation_id=conversation.id,
    user_id="user123",
    limit=10  # Get last 10 messages for context
)
```

### Searching Messages
```python
search_results, total = await service.search_messages_in_conversation(
    conversation_id=conversation.id,
    user_id="user123",
    search_term="groceries",
    role="user",  # Optional: filter by role
    limit=20
)
```

### Deleting User's Conversations (on account deletion)
```python
deleted_count = await service.delete_conversations_for_user(user_id="user123")
```

## Security Features

### Authentication & Authorization
- All endpoints require valid user authentication
- Users can only access their own conversations and messages
- Conversation ownership is validated for every operation

### Data Isolation
- Database-level foreign key constraints ensure data integrity
- Cascade delete removes messages when conversations are deleted
- Check constraints enforce valid message roles

## Troubleshooting

### Migration Issues
If you encounter migration errors:
1. Check that PostgreSQL is running
2. Verify database connection settings
3. Run `alembic current` to check current migration state

### Authentication Issues
If API calls return 401 errors:
1. Ensure you're sending proper authentication headers
2. Verify that the user session is valid
3. Check that the authentication middleware is properly configured

### Rate Limiting
If requests are being rejected due to rate limiting:
1. Check the response headers for rate limit information
2. Implement appropriate client-side rate limiting
3. Consider if legitimate usage patterns might trigger false positives