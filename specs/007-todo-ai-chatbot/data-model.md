# Data Model: Todo AI Chatbot - Database Schema for Conversations

## Conversation Entity

**Description**: Represents a chat session for a specific user, containing metadata about the session including creation and update timestamps.

**Fields**:
- `id`: Primary key, auto-increment integer
- `user_id`: Foreign key to users table, string/varchar (indexed)
- `created_at`: Timestamp when conversation started (default: current timestamp)
- `updated_at`: Timestamp of last message in conversation (indexed, auto-updating)

**Relationships**:
- One-to-many with Message entity (one conversation to many messages)
- Many-to-one with User entity (many conversations to one user)
- Cascade delete: When user is deleted, all associated conversations are removed

**Validation Rules**:
- `user_id` must reference an existing user
- `created_at` must be before or equal to `updated_at`
- `user_id` cannot be null

## Message Entity

**Description**: Represents an individual communication within a conversation, including the sender role, content, and any tools called during processing.

**Fields**:
- `id`: Primary key, auto-increment integer
- `conversation_id`: Foreign key to conversations table (indexed)
- `user_id`: Foreign key to users table, string/varchar (indexed)
- `role`: Enum/string: 'user', 'assistant', or 'system' (with check constraint)
- `content`: Text field for message content (cannot be null/empty)
- `tool_calls`: JSON/JSONB field for storing which MCP tools were called (nullable)
- `created_at`: Timestamp when message was created (default: current timestamp, indexed)

**Relationships**:
- Many-to-one with Conversation entity (many messages to one conversation)
- Many-to-one with User entity (many messages to one user)
- Cascade delete: When conversation is deleted, all associated messages are removed

**Validation Rules**:
- `conversation_id` must reference an existing conversation
- `user_id` must reference an existing user
- `role` must be one of 'user', 'assistant', or 'system'
- `content` cannot be null
- `conversation_id` and `user_id` must be consistent (message belongs to conversation owned by user)

## State Transitions

**Conversation**:
- Created when first message is sent by user
- Updated when new messages are added (updated_at timestamp changes)
- Deleted when user account is deleted (cascade delete)

**Message**:
- Created when a new message is sent in a conversation
- Never modified after creation (immutable design for conversation integrity)
- Deleted when parent conversation is deleted (cascade delete)

## Constraints and Indexes

**Conversations Table**:
- Primary Key: `id`
- Foreign Key: `user_id` → users.id (CASCADE DELETE)
- Indexes: `user_id`, `updated_at`
- Check Constraints: None

**Messages Table**:
- Primary Key: `id`
- Foreign Keys:
  - `conversation_id` → conversations.id (CASCADE DELETE)
  - `user_id` → users.id
- Indexes: `conversation_id`, `created_at`, `user_id`
- Check Constraints: `role` IN ('user', 'assistant', 'system')

## API Access Patterns

**Common Queries**:
1. Get all conversations for a user (filtered by user_id, ordered by updated_at DESC)
2. Get all messages for a conversation (filtered by conversation_id, ordered by created_at ASC)
3. Create a new conversation (insert into conversations table)
4. Add a message to a conversation (insert into messages table)
5. Update conversation timestamp (update conversations.updated_at)

**Performance Considerations**:
- Indexes support the most common query patterns
- Foreign key constraints ensure data integrity
- Cascade deletes maintain referential integrity automatically