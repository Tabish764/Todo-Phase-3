# Data Model: Fix AI Chatbot Integration Issues

## Entities

### ChatMessage
- **Description**: Represents a single message in a conversation
- **Fields**:
  - id (string): Unique identifier for the message
  - role (string): Either 'user' or 'assistant' to identify the sender
  - content (string): The actual message content
  - timestamp (date): When the message was created/sent
  - tool_calls (array): Optional array of tool calls executed as part of this message
  - conversation_id (number): Reference to the conversation this message belongs to

### Conversation
- **Description**: Represents a single conversation thread between user and AI
- **Fields**:
  - id (number): Unique identifier for the conversation
  - user_id (string): Reference to the user who owns this conversation
  - title (string): Generated from the first message or user-provided
  - created_at (date): When the conversation was started
  - updated_at (date): When the last message was sent in this conversation
  - is_active (boolean): Whether this conversation is currently active

### Task
- **Description**: Represents a user task managed by the system
- **Fields**:
  - id (number): Unique identifier for the task
  - user_id (string): Reference to the user who owns this task
  - title (string): Task description/title
  - description (string): Additional details about the task
  - completed (boolean): Whether the task is completed
  - created_at (date): When the task was created
  - updated_at (date): When the task was last updated

## Relationships

### Conversation ↔ ChatMessage
- **Type**: One-to-Many
- **Description**: A conversation contains multiple messages
- **Constraint**: All messages in a conversation must belong to the same user

### User ↔ Conversation
- **Type**: One-to-Many
- **Description**: A user can have multiple conversations
- **Constraint**: Conversations are user-isolated (one user cannot access another's conversations)

### User ↔ Task
- **Type**: One-to-Many
- **Description**: A user can have multiple tasks
- **Constraint**: Tasks are user-isolated (one user cannot access another's tasks)

## Validation Rules

### ChatMessage Validation
- content must not be empty
- role must be either 'user' or 'assistant'
- timestamp must be a valid date/time
- conversation_id must reference an existing conversation

### Conversation Validation
- title must not exceed 200 characters
- user_id must reference an existing user
- created_at must be before or equal to updated_at

### Task Validation
- title must not be empty
- user_id must reference an existing user
- completed must be a boolean value

## State Transitions

### Task State Transitions
- pending → completed (when complete_task tool is executed)
- completed → pending (when update_task tool is executed with completed=false)

## API Endpoints

### Chat API
- `POST /api/{user_id}/chat` - Send a message and receive AI response
- `GET /api/{user_id}/conversations` - Get list of user's conversations
- `GET /api/{user_id}/conversations/{conversation_id}/messages` - Get messages in a specific conversation

### Task API
- `GET /api/{user_id}/tasks` - Get user's tasks with optional status filter
- `POST /api/{user_id}/tasks` - Create a new task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task