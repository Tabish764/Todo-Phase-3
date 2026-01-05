# Feature Specification: Todo AI Chatbot - Chat API Endpoint

**Feature Branch**: `009-chat-api-endpoint`
**Created**: 2025-12-27
**Status**: Draft
**Dependencies**:
- Feature 007: Database Schema (conversations, messages tables)
- Feature 008: MCP Server Tools (add_task, list_tasks, complete_task, delete_task, update_task)

## Overview

Build a stateless FastAPI endpoint that receives chat messages from the frontend, orchestrates AI agent interactions with MCP tools, persists all conversation data to the database, and returns responses to the client.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Send Message and Receive AI Response (Priority: P1)

As a user of the todo chatbot, I want to send a natural language message and receive an intelligent response so that I can manage my tasks through conversation.

**Why this priority**: This is the core functionality of the entire Phase III. Without this endpoint working, users cannot interact with the AI chatbot at all.

**Independent Test**: Can be tested by sending a POST request to the chat endpoint with a simple message like "Hello" and verifying a response is returned with proper conversation_id.

**Acceptance Scenarios**:

1. **Given** a user sends their first message, **When** the endpoint receives the request, **Then** a new conversation is created in the database and the AI responds appropriately
2. **Given** a user sends a message with an existing conversation_id, **When** the endpoint receives the request, **Then** the full conversation history is loaded and the AI responds with proper context
3. **Given** a user sends a task-related message, **When** the AI agent processes it, **Then** the appropriate MCP tool is called and the result is reflected in the response

---

### User Story 2 - Stateless Request Processing (Priority: P1)

As a system administrator, I want the chat endpoint to be completely stateless so that any server instance can handle any request, enabling horizontal scaling and resilience.

**Why this priority**: Stateless architecture is a fundamental requirement stated in Phase III specifications. Without this, the system cannot scale or recover from server restarts.

**Independent Test**: Can be tested by starting a conversation on one server instance, restarting the server, and continuing the conversation - the AI should maintain full context from database-stored history.

**Acceptance Scenarios**:

1. **Given** the server restarts mid-conversation, **When** the user sends their next message, **Then** the endpoint retrieves conversation history from database and continues seamlessly
2. **Given** multiple server instances are running, **When** requests from the same conversation hit different instances, **Then** each instance retrieves the same conversation state from database and responds consistently
3. **Given** a request is processed, **When** the endpoint completes its work, **Then** no conversation state is stored in server memory

---

### User Story 3 - Conversation History Persistence (Priority: P2)

As a user having a conversation with the AI chatbot, I want every message and response to be saved to the database so that I can reference past interactions and the AI maintains context across sessions.

**Why this priority**: This enables the AI to understand references to previous messages and allows users to resume conversations after closing the app.

**Independent Test**: Can be tested by having a multi-turn conversation, then querying the database directly to verify all user and assistant messages are stored with correct timestamps and conversation_id.

**Acceptance Scenarios**:

1. **Given** a user sends a message, **When** the endpoint processes it, **Then** the user's message is stored in the messages table with role='user' before the AI processes it
2. **Given** the AI agent generates a response, **When** the endpoint receives it, **Then** the assistant's message is stored in the messages table with role='assistant' and any tool_calls recorded
3. **Given** multiple messages in a conversation, **When** querying the database, **Then** all messages are stored in chronological order with proper conversation_id linking

---

### User Story 4 - AI Agent Integration with MCP Tools (Priority: P1)

As a user giving task management commands, I want the AI to understand my intent and automatically call the appropriate MCP tools so that I can manage tasks without knowing technical details.

**Why this priority**: This is the bridge between natural language and task operations. Without this, the AI cannot actually perform task management actions.

**Independent Test**: Can be tested by sending commands like "Add buy groceries" and verifying that the add_task MCP tool is called with correct parameters and the task appears in the database.

**Acceptance Scenarios**:

1. **Given** a user says "Add a task to buy milk", **When** the AI agent processes the message, **Then** the add_task MCP tool is called with title="Buy milk"
2. **Given** a user says "Show my pending tasks", **When** the AI agent processes the message, **Then** the list_tasks MCP tool is called with status="pending"
3. **Given** the AI calls an MCP tool, **When** the tool returns results, **Then** those results are included in the AI's natural language response to the user

---

### User Story 5 - Error Handling and Graceful Degradation (Priority: P2)

As a user, I want clear error messages when something goes wrong so that I understand what happened and can take appropriate action.

**Why this priority**: Good error handling ensures users aren't left confused when failures occur and helps with debugging during development.

**Independent Test**: Can be tested by simulating various failure scenarios (database down, invalid conversation_id, AI API failure) and verifying appropriate error responses are returned.

**Acceptance Scenarios**:

1. **Given** a user provides an invalid conversation_id, **When** the endpoint tries to fetch it, **Then** a 404 error is returned with message "Conversation not found"
2. **Given** a user sends an empty message, **When** the endpoint validates the request, **Then** a 400 error is returned with message "Message cannot be empty"
3. **Given** the database is unavailable, **When** the endpoint tries to persist data, **Then** a 503 error is returned with message "Service temporarily unavailable"
4. **Given** the AI agent fails to process a message, **When** the error occurs, **Then** a user-friendly error response is returned and partial data is saved if possible

---

### Edge Cases

- What happens when a user references a conversation_id that belongs to a different user?
- How does the system handle extremely long messages (e.g., 10,000 characters)?
- What occurs when the AI agent takes longer than expected to respond (timeout scenarios)?
- How does the system handle concurrent requests to the same conversation from the same user?
- What happens when the MCP server is unavailable but the database is accessible?
- How does the endpoint handle malformed JSON in the request body?
- What occurs when the AI agent returns an empty or null response?
- How does the system handle database write failures after the AI has already generated a response?

---

## Requirements *(mandatory)*

### Functional Requirements

#### Endpoint Specification

- **FR-001**: Endpoint MUST be accessible at `POST /api/{user_id}/chat`
- **FR-002**: Endpoint MUST accept path parameter `user_id` (string) to identify the requesting user
- **FR-003**: Endpoint MUST accept JSON request body with fields:
  - `message` (string, required): User's natural language message
  - `conversation_id` (integer, optional): Existing conversation to continue
- **FR-004**: Endpoint MUST return JSON response with fields:
  - `conversation_id` (integer): The conversation ID (new or existing)
  - `response` (string): AI assistant's natural language response
  - `tool_calls` (array, optional): List of MCP tools invoked with their results

#### Request Processing Flow

- **FR-005**: System MUST validate that the user_id exists in the database before processing
- **FR-006**: System MUST validate that the message field is not empty or null
- **FR-007**: If conversation_id is provided, system MUST verify the conversation exists and belongs to the user_id
- **FR-008**: If conversation_id is not provided, system MUST create a new conversation record with the user_id
- **FR-009**: System MUST fetch all messages for the conversation ordered by created_at ascending
- **FR-010**: System MUST store the user's message in the messages table with role='user' before invoking the AI agent
- **FR-011**: System MUST build a message array for the AI agent containing:
  - System instruction message (if first message in conversation)
  - All historical messages from the conversation
  - The current user message
- **FR-012**: System MUST pass the MCP tools configuration to the AI agent so tools can be invoked
- **FR-013**: System MUST invoke the AI agent with the message array and available MCP tools
- **FR-014**: System MUST capture all MCP tool calls made by the AI agent including tool name, arguments, and results
- **FR-015**: System MUST store the AI's response in the messages table with role='assistant' and tool_calls as JSONB
- **FR-016**: System MUST update the conversation's updated_at timestamp to current time
- **FR-017**: System MUST return the response to the client with conversation_id, response text, and tool_calls
- **FR-018**: System MUST NOT maintain any conversation state in server memory between requests

#### Error Handling

- **FR-019**: System MUST return HTTP 400 if message field is missing or empty
- **FR-020**: System MUST return HTTP 401 if user_id is invalid or unauthorized
- **FR-021**: System MUST return HTTP 404 if conversation_id is provided but doesn't exist
- **FR-022**: System MUST return HTTP 403 if conversation_id exists but belongs to different user
- **FR-023**: System MUST return HTTP 500 if AI agent fails to process the message
- **FR-024**: System MUST return HTTP 503 if database is unavailable
- **FR-025**: System MUST log all errors with sufficient detail for debugging
- **FR-026**: System MUST return error responses in JSON format with fields:
  - `error` (string): Error type/code
  - `message` (string): Human-readable error description
  - `details` (object, optional): Additional error context

#### Performance Requirements

- **FR-027**: System MUST respond to requests within 10 seconds under normal load
- **FR-028**: System MUST handle at least 100 concurrent requests without degradation
- **FR-029**: System MUST use database connection pooling for efficient resource usage
- **FR-030**: System MUST implement request timeouts to prevent hung requests

### Key Entities *(include if feature involves data)*

- **ChatRequest**: Input data containing user_id, optional conversation_id, and message text
- **ChatResponse**: Output data containing conversation_id, AI response text, and optional tool_calls
- **MessageContext**: The full array of messages sent to the AI agent, including system instructions and conversation history
- **ToolCall**: Record of an MCP tool invocation including tool name, input arguments, and output results

---

## Technical Specifications

### Request Format

```
POST /api/{user_id}/chat
Content-Type: application/json

{
  "conversation_id": 123,  // optional, omit for new conversation
  "message": "Add a task to buy groceries"
}
```

### Response Format (Success)

```
HTTP 200 OK
Content-Type: application/json

{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your task list!",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "arguments": {
        "user_id": "user123",
        "title": "Buy groceries"
      },
      "result": {
        "task_id": 5,
        "status": "created",
        "title": "Buy groceries"
      }
    }
  ]
}
```

### Response Format (Error)

```
HTTP 400 Bad Request
Content-Type: application/json

{
  "error": "INVALID_REQUEST",
  "message": "Message cannot be empty",
  "details": {
    "field": "message",
    "constraint": "non_empty"
  }
}
```

### Processing Sequence

**Step 1: Validate Request**
- Check user_id exists
- Check message is not empty
- If conversation_id provided, verify it exists and belongs to user

**Step 2: Initialize or Load Conversation**
- If no conversation_id: Create new conversation record, get new ID
- If conversation_id: Fetch existing conversation record
- Fetch all messages for conversation (ordered by created_at)

**Step 3: Store User Message**
- Insert message record:
  - conversation_id: current conversation ID
  - user_id: from path parameter
  - role: 'user'
  - content: from request body
  - created_at: current timestamp

**Step 4: Build AI Agent Context**
- Create message array:
  - [0] System message with agent instructions (if first message)
  - [1..n] All historical messages (user and assistant)
  - [n+1] Current user message
- Prepare MCP tools configuration

**Step 5: Invoke AI Agent**
- Call Gemini API with message array and tools
- AI agent processes message
- AI agent may invoke zero or more MCP tools
- AI agent generates natural language response
- Capture all tool calls with arguments and results

**Step 6: Store Assistant Response**
- Insert message record:
  - conversation_id: current conversation ID
  - user_id: from path parameter
  - role: 'assistant'
  - content: AI's response text
  - tool_calls: JSONB array of tool invocations
  - created_at: current timestamp

**Step 7: Update Conversation**
- Update conversation.updated_at to current timestamp

**Step 8: Return Response**
- Build response JSON with conversation_id, response, tool_calls
- Return HTTP 200 with response body

**Step 9: Cleanup**
- Close database connections
- No state retained in memory

### Stateless Architecture Requirements

**No Session Storage:**
- Endpoint does not use sessions, cookies, or in-memory cache
- All state retrieved from database on every request

**Database as Single Source of Truth:**
- Conversation history always fetched from database
- Messages always stored to database immediately
- No assumptions about previous requests

**Scalability Implications:**
- Any server instance can handle any request
- Load balancer can distribute freely
- Server restarts have zero impact on conversations
- Horizontal scaling is trivial

### Integration Points

**With Database (via SQLModel):**
- Read: conversations, messages, users tables
- Write: conversations (create/update), messages (insert)
- Transaction handling for data consistency

**With AI Agent (Gemini API):**
- Send: Message array and MCP tools configuration
- Receive: Response text and tool call records
- Handle: API errors, timeouts, rate limits

**With MCP Server:**
- Agent invokes tools during processing
- Tools are defined in MCP server configuration
- Tool results returned synchronously to agent

**With Frontend (ChatKit):**
- Receive: HTTP POST requests with JSON body
- Send: HTTP responses with JSON body
- Handle: CORS headers for browser access

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chat endpoint responds to 99.9% of valid requests within 10 seconds
- **SC-002**: 100% of user messages are successfully stored in database before AI processing begins
- **SC-003**: 100% of AI responses are successfully stored in database before being returned to client
- **SC-004**: Endpoint correctly handles at least 100 concurrent requests without data corruption
- **SC-005**: Conversation context is preserved across server restarts in 100% of cases
- **SC-006**: System correctly creates new conversations when conversation_id is not provided
- **SC-007**: System correctly loads existing conversation history when conversation_id is provided
- **SC-008**: System correctly rejects requests with invalid conversation_id or user_id mismatch
- **SC-009**: All MCP tool calls are correctly recorded in the assistant message's tool_calls field
- **SC-010**: Error responses include clear, actionable messages in 100% of error cases

### Quality Metrics

- **QM-001**: Average response time under 5 seconds for simple queries
- **QM-002**: Average response time under 8 seconds for complex queries requiring multiple tool calls
- **QM-003**: Zero conversation history loss during normal operation
- **QM-004**: Error rate below 0.1% for valid requests
- **QM-005**: Database queries optimized to prevent N+1 problems when fetching conversation history

### Testing Requirements

- **TR-001**: Unit tests for request validation logic
- **TR-002**: Unit tests for conversation creation/loading logic
- **TR-003**: Integration tests for full request-response cycle
- **TR-004**: Integration tests for AI agent and MCP tool invocation
- **TR-005**: Integration tests for database persistence
- **TR-006**: Load tests demonstrating 100 concurrent requests
- **TR-007**: Failure tests for database unavailability
- **TR-008**: Failure tests for AI agent errors
- **TR-009**: Failure tests for invalid request data
- **TR-010**: Statelessness tests with server restarts