# Data Model: Todo AI Chatbot - Chat API Endpoint

## Entity: Conversation
- **Fields**:
  - id: Integer (Primary Key, Auto-increment)
  - user_id: String (Foreign Key reference to user)
  - created_at: DateTime (Default: current timestamp)
  - updated_at: DateTime (Default: current timestamp, updates on modification)
  - title: String (Optional, auto-generated from first message or AI response)

- **Validation Rules**:
  - user_id must exist in users table
  - created_at and updated_at are automatically managed
  - title is optional, can be auto-generated

- **Relationships**:
  - One-to-Many: Conversation → Messages

## Entity: Message
- **Fields**:
  - id: Integer (Primary Key, Auto-increment)
  - conversation_id: Integer (Foreign Key reference to conversation)
  - user_id: String (Reference to user who sent the message)
  - role: String (Enum: 'user' | 'assistant')
  - content: String (Text content of the message)
  - tool_calls: JSONB (Optional, JSON array of tool calls made by assistant)
  - created_at: DateTime (Default: current timestamp)

- **Validation Rules**:
  - conversation_id must exist in conversations table
  - role must be either 'user' or 'assistant'
  - content cannot be empty
  - tool_calls must be valid JSON when present

- **Relationships**:
  - Many-to-One: Message → Conversation
  - One-to-Many: Message → ToolCall (embedded in JSONB)

## Entity: ToolCall (Embedded in Message)
- **Fields** (as part of tool_calls JSONB array):
  - tool_name: String (Name of the MCP tool called)
  - arguments: Object (Arguments passed to the tool)
  - result: Object (Result returned by the tool)

- **Validation Rules**:
  - tool_name must be one of the registered MCP tools
  - arguments must match the expected schema for the tool
  - result must be valid response from the tool

## State Transitions
- Conversation: Created when first user message is received
- Message: Created when user sends a message (role='user') or AI responds (role='assistant')
- Conversation.updated_at: Updated whenever a new message is added to the conversation

## Indexes
- Conversation: Index on user_id for efficient user conversation retrieval
- Message: Index on conversation_id for efficient conversation history retrieval
- Message: Index on created_at for chronological ordering