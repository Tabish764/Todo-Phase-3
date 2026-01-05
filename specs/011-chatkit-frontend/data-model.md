# Data Model: Todo AI Chatbot - ChatKit Frontend UI

## Overview
Data model for the frontend UI components, defining the structure of data passed between components and exchanged with the backend API.

## Core Entities

### ChatMessage
**Description**: Represents a single message in the chat interface

**Fields**:
- `id` (string | number): Unique identifier for the message
- `role` (MessageRole): Either 'user' or 'assistant'
- `content` (string): The message text content
- `timestamp` (Date | string): When the message was created/sent
- `tool_calls` (ToolCall[] | null): Optional array of tool calls made by the assistant
- `isLoading` (boolean): For user messages, indicates if waiting for response
- `error` (string | null): Optional error message if the message failed to send

**Validation Rules**:
- `id` must be unique within the conversation
- `role` must be one of the allowed values
- `content` must not be empty
- `timestamp` must be a valid date

### MessageRole
**Description**: Enum representing the role of a message sender

**Values**:
- `user`: Message sent by the user
- `assistant`: Message sent by the AI assistant

### Conversation
**Description**: Represents a conversation context in the UI

**Fields**:
- `id` (number): Unique identifier for the conversation
- `title` (string): Display title for the conversation (often first message or AI-generated)
- `lastUpdated` (Date): Timestamp of the last message in the conversation
- `messageCount` (number): Number of messages in the conversation
- `preview` (string): Short preview text for the conversation list

**Validation Rules**:
- `id` must be unique across all conversations
- `title` must not exceed 100 characters
- `lastUpdated` must be a valid date

### ChatState
**Description**: Represents the current state of the chat interface

**Fields**:
- `currentConversationId` (number | null): ID of the active conversation
- `messages` (ChatMessage[]): Array of messages in the current conversation
- `inputText` (string): Current value of the message input field
- `isLoading` (boolean): Whether the app is waiting for an AI response
- `error` (string | null): Current error state
- `conversations` (Conversation[]): List of available conversations
- `sidebarOpen` (boolean): Whether the conversation sidebar is open

**Validation Rules**:
- `messages` array must maintain chronological order
- `isLoading` and `error` should not both be true simultaneously

### APIRequest
**Description**: Structure of requests sent to the backend API

**Fields**:
- `user_id` (string): Identifier of the current user
- `conversation_id` (number | null): ID of the conversation (null for new conversations)
- `message` (string): The message content to send

**Validation Rules**:
- `user_id` must be provided
- `message` must not be empty after trimming
- `conversation_id` must be positive if provided

### APIResponse
**Description**: Structure of responses received from the backend API

**Fields**:
- `conversation_id` (number): ID of the conversation (newly created or existing)
- `response` (string): The AI's response message
- `tool_calls` (ToolCall[] | null): Optional array of tool calls made by the AI

**Validation Rules**:
- `conversation_id` must be provided
- `response` must be provided

### ToolCall
**Description**: Represents a tool call made by the AI assistant

**Fields**:
- `name` (string): Name of the tool that was called
- `arguments` (object): Arguments passed to the tool
- `result` (object): Result of the tool call

**Validation Rules**:
- `name` must be a valid tool name
- `arguments` and `result` must be valid JSON objects

## State Transitions

### Chat Interface States
1. **Initial State**: No conversation selected, empty message list
   - `currentConversationId`: null
   - `messages`: []
   - `isLoading`: false

2. **New Conversation**: User starts a new conversation
   - `currentConversationId`: newly assigned ID
   - `messages`: [userMessage]
   - `isLoading`: true (waiting for first AI response)

3. **Active Conversation**: User and AI exchanging messages
   - `currentConversationId`: existing conversation ID
   - `messages`: [message1, message2, ...]
   - `isLoading`: true when waiting for AI response

4. **Error State**: An error occurred during communication
   - `currentConversationId`: existing conversation ID
   - `messages`: current messages
   - `isLoading`: false
   - `error`: error message string

## UI-Specific Models

### MessageDisplay
**Description**: Enhanced message data for UI rendering

**Fields**:
- `id` (string | number): Unique identifier
- `role` (MessageRole): User or assistant
- `content` (string): Message content
- `timestamp` (Date): When sent
- `formattedContent` (string): HTML-formatted content for display
- `isExpanded` (boolean): For tool calls, whether details are shown
- `isPending` (boolean): Whether message is still being processed

### ConversationListItem
**Description**: Data structure for displaying conversations in the sidebar

**Fields**:
- `id` (number): Conversation ID
- `title` (string): Display title
- `lastMessagePreview` (string): Preview of the last message
- `lastUpdated` (Date): When last active
- `isActive` (boolean): Whether this is the current conversation
- `unreadCount` (number): Number of unread messages (optional)

## API Contract Models

### Request Models

#### SendMessageRequest
- `user_id`: string (required)
- `conversation_id`: number (optional, null for new conversation)
- `message`: string (required, trimmed)

#### GetConversationsRequest
- `user_id`: string (required)

#### GetConversationHistoryRequest
- `user_id`: string (required)
- `conversation_id`: number (required)

### Response Models

#### SendMessageResponse
- `conversation_id`: number (required)
- `response`: string (required)
- `tool_calls`: ToolCall[] | null (optional)

#### GetConversationsResponse
- `conversations`: Conversation[] (required)

#### GetConversationHistoryResponse
- `messages`: ChatMessage[] (required)