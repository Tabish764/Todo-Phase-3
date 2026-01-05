# API Contract: Chat Service

## Overview
This document defines the API contract for the chat service that enables communication between the frontend chat interface and the backend AI processing system.

## Base URL
`http://localhost:8000/api` (development) or `https://api.yourapp.com/api` (production)

## Authentication
All endpoints require a valid Better Auth session token passed in the Authorization header:
```
Authorization: Bearer <session_token>
```

## Endpoints

### POST /{user_id}/chat
Send a message to the AI assistant and receive a response.

#### Request
**Headers:**
- `Authorization: Bearer <session_token>`
- `Content-Type: application/json`

**Body:**
```json
{
  "conversation_id": 123,
  "message": "Hello, can you help me add a task?"
}
```

**Fields:**
- `conversation_id` (optional, number): ID of the existing conversation; if not provided, a new conversation is created
- `message` (required, string): The user's message to the AI

#### Response
**Success (200 OK):**
```json
{
  "conversation_id": 123,
  "response": "Sure, what task would you like to add?",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "arguments": {
        "title": "Buy groceries",
        "user_id": "user123"
      },
      "result": {
        "task_id": 456,
        "status": "created",
        "title": "Buy groceries"
      }
    }
  ]
}
```

**Error Responses:**
- `400 Bad Request`: Invalid request format or missing required fields
- `401 Unauthorized`: Invalid or expired session token
- `404 Not Found`: User_id or conversation_id not found
- `500 Internal Server Error`: Server processing error

### GET /{user_id}/conversations
Retrieve a list of conversations for the specified user.

#### Request
**Headers:**
- `Authorization: Bearer <session_token>`

#### Response
**Success (200 OK):**
```json
[
  {
    "id": 123,
    "title": "Task management help",
    "created_at": "2023-12-30T10:00:00Z",
    "updated_at": "2023-12-30T11:30:00Z"
  },
  {
    "id": 124,
    "title": "Project planning",
    "created_at": "2023-12-29T09:15:00Z",
    "updated_at": "2023-12-29T14:20:00Z"
  }
]
```

### GET /{user_id}/conversations/{conversation_id}/messages
Retrieve the message history for a specific conversation.

#### Request
**Headers:**
- `Authorization: Bearer <session_token>`

#### Response
**Success (200 OK):**
```json
[
  {
    "id": "msg-1",
    "role": "user",
    "content": "Can you help me add a task?",
    "timestamp": "2023-12-30T10:00:00Z"
  },
  {
    "id": "msg-2",
    "role": "assistant",
    "content": "Sure, what task would you like to add?",
    "timestamp": "2023-12-30T10:00:05Z",
    "tool_calls": []
  }
]
```

## Error Response Format
All error responses follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details (optional)"
  }
}
```

## Common Error Codes
- `INVALID_REQUEST`: Request format is invalid
- `AUTHENTICATION_FAILED`: Session token is invalid or expired
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `TOOL_EXECUTION_FAILED`: AI tool execution failed
- `INTERNAL_ERROR`: Server-side processing error

## Rate Limits
- 100 requests per minute per user
- 1000 requests per minute per IP (unauthenticated)

## Version
API Version: 1.0