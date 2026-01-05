# Chat API Documentation

## Overview

The Chat API provides a stateless endpoint for users to interact with an AI assistant that can manage tasks through MCP tools.

## API Endpoints

### POST /api/{user_id}/chat

Receives chat messages from the frontend, orchestrates AI agent interactions with MCP tools, persists conversation data to the database, and returns responses to the client.

#### Path Parameters

- `user_id` (string, required): The ID of the requesting user

#### Request Body

```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

#### Response

**Success Response (200 OK)**

```json
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

**Error Responses**

- 400 Bad Request: Invalid request
- 401 Unauthorized: Invalid user
- 403 Forbidden: Access to conversation denied
- 404 Not Found: Conversation not found
- 500 Internal Server Error: AI service error
- 503 Service Unavailable: Database unavailable

## Architecture

### Stateless Design

The API is completely stateless:
- All conversation history is retrieved from the database on each request
- No server-side session storage
- Any server instance can handle any request
- Conversation context preserved across server restarts

### Data Flow

1. Validate request parameters
2. Load conversation history from database (if conversation_id provided)
3. Store user message in database before AI processing
4. Build message array with conversation history for AI agent
5. Invoke AI agent with available MCP tools
6. Store AI response in database after processing
7. Return response to client
