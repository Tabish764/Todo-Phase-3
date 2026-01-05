# Data Model: Todo AI Chatbot Implementation Fixes

## Overview
Data model for the Todo AI Chatbot application, defining the structure of entities for tasks, conversations, and messages with proper relationships and validation rules.

## Core Entities

### Task
**Description**: Represents a single task in the user's todo list

**Fields**:
- `id` (Integer): Unique identifier for the task (primary key, auto-increment)
- `user_id` (String): Identifier for the user who owns the task (foreign key)
- `title` (String): The main description of the task (required, max 255 characters)
- `description` (String): Additional details about the task (optional, max 1000 characters)
- `completed` (Boolean): Status of task completion (default: false)
- `created_at` (DateTime): Timestamp when the task was created (default: now)
- `updated_at` (DateTime): Timestamp when the task was last modified (default: now)

**Validation Rules**:
- `id` must be unique across all tasks
- `user_id` must reference a valid user
- `title` must not be empty after trimming
- `title` must not exceed 255 characters
- `completed` defaults to false when creating new tasks
- `created_at` must be a valid timestamp
- `updated_at` must be updated when the task is modified

**Relationships**:
- Belongs to one User
- No direct relationships to other entities

### Conversation
**Description**: Represents a conversation context containing multiple messages

**Fields**:
- `id` (Integer): Unique identifier for the conversation (primary key, auto-increment)
- `user_id` (String): Identifier for the user who owns the conversation (foreign key)
- `title` (String): Display title for the conversation (optional, auto-generated from first message)
- `created_at` (DateTime): Timestamp when the conversation was started (default: now)
- `updated_at` (DateTime): Timestamp when the conversation was last active (default: now)

**Validation Rules**:
- `id` must be unique across all conversations
- `user_id` must reference a valid user
- `title` may be auto-generated if not provided
- `created_at` must be a valid timestamp
- `updated_at` must be updated when messages are added

**Relationships**:
- Belongs to one User
- Has many Messages

### Message
**Description**: Represents a single message in a conversation

**Fields**:
- `id` (Integer): Unique identifier for the message (primary key, auto-increment)
- `conversation_id` (Integer): Identifier for the conversation this message belongs to (foreign key)
- `user_id` (String): Identifier for the user who sent the message (foreign key)
- `role` (Enum): Role of the message sender (user or assistant)
- `content` (String): The text content of the message (required)
- `tool_calls` (JSON): Optional array of tool calls made by the assistant (JSON field)
- `created_at` (DateTime): Timestamp when the message was created (default: now)

**Validation Rules**:
- `id` must be unique across all messages
- `conversation_id` must reference a valid conversation
- `user_id` must reference a valid user
- `role` must be one of the allowed values (user, assistant)
- `content` must not be empty after trimming
- `tool_calls` must be valid JSON if provided
- `created_at` must be a valid timestamp

**Relationships**:
- Belongs to one Conversation
- Belongs to one User

## State Transitions

### Task State Transitions
1. **Created**: Task is added to user's list with `completed = false`
2. **Completed**: Task is marked as complete with `completed = true`
3. **Updated**: Task details (title, description) are modified
4. **Deleted**: Task is removed from user's list

### Conversation State Transitions
1. **Started**: New conversation created with first message
2. **Active**: Messages are exchanged between user and assistant
3. **Inactive**: No new messages for extended period (still accessible)

### Message State Transitions
1. **Created**: Message is added to conversation with content
2. **Processed**: AI agent processes message and may call tools
3. **Responded**: Assistant response is added to conversation

## API Request/Response Models

### ChatRequest
**Description**: Structure of requests sent to the chat API endpoint

**Fields**:
- `conversation_id` (Integer, optional): ID of existing conversation (creates new if not provided)
- `message` (String): The user's message content (required, 1-10000 characters)

**Validation Rules**:
- `message` must not be empty after trimming
- `message` must not exceed 10000 characters
- `conversation_id` must be positive if provided

### ChatResponse
**Description**: Structure of responses from the chat API endpoint

**Fields**:
- `conversation_id` (Integer): ID of the conversation (newly created or existing)
- `response` (String): The AI's response message
- `tool_calls` (Array of ToolCall objects, optional): Array of tools called by the AI

**Validation Rules**:
- `conversation_id` must be provided
- `response` must be provided
- `tool_calls` must be valid array of tool call objects if present

### ToolCall
**Description**: Represents a tool call made by the AI assistant

**Fields**:
- `tool_name` (String): Name of the tool that was called
- `arguments` (Object): Arguments passed to the tool
- `result` (Object): Result of the tool call

**Validation Rules**:
- `tool_name` must be a valid tool name
- `arguments` must be valid JSON object
- `result` must be valid JSON object

## Database Constraints

### Primary Keys
- Each entity has an auto-incrementing integer primary key
- Primary keys are unique and non-null

### Foreign Keys
- `user_id` in Task, Conversation, and Message references User table
- `conversation_id` in Message references Conversation table

### Indexes
- Index on `user_id` for all entities for efficient user-based queries
- Index on `conversation_id` in Message table for efficient conversation queries
- Index on `created_at` for chronological ordering

## Validation Rules Summary

### Task Validation
- Title required and ≤ 255 chars
- User ID must exist
- Completed defaults to false

### Conversation Validation
- User ID must exist
- Messages linked properly
- Timestamps maintained

### Message Validation
- Content required
- Valid role (user/assistant)
- Linked to valid conversation
- Proper tool call format