# API Contract: Todo AI Chatbot - ChatKit Frontend UI

## Overview
API contract defining the interface between the frontend ChatKit UI and the backend services.

## Endpoints

### POST /api/{user_id}/chat
Send a message and receive an AI response.

#### Request
- **Method**: POST
- **Path**: `/api/{user_id}/chat`
- **Path Parameters**:
  - `user_id` (string): The ID of the requesting user
- **Headers**:
  - `Content-Type`: `application/json`
  - `Authorization`: Bearer token (if required)
- **Body**:
  ```json
  {
    "conversation_id": 123,
    "message": "Hello, add buy milk to my tasks"
  }
  ```
- **Body Schema**:
  - `conversation_id` (integer, optional): ID of the existing conversation. If not provided, a new conversation will be created.
  - `message` (string, required): The message content. Must be between 1 and 10000 characters.

#### Response
- **Success Response (200 OK)**:
  ```json
  {
    "conversation_id": 123,
    "response": "I've added 'buy milk' to your task list!",
    "tool_calls": [
      {
        "tool_name": "add_task",
        "arguments": {
          "user_id": "user123",
          "title": "buy milk"
        },
        "result": {
          "task_id": 456,
          "status": "created"
        }
      }
    ]
  }
  ```
- **Response Schema**:
  - `conversation_id` (integer): The ID of the conversation (newly created or existing)
  - `response` (string): The AI's response message
  - `tool_calls` (array of objects, optional): Array of tool calls made by the AI

- **Error Responses**:
  - `400 Bad Request`: Invalid request format or missing required fields
    ```json
    {
      "error": "INVALID_INPUT",
      "message": "Message cannot be empty",
      "details": {
        "field": "message"
      }
    }
    ```
  - `401 Unauthorized`: Invalid or missing authentication
  - `404 Not Found`: Conversation ID does not exist
  - `500 Internal Server Error`: Server error processing the request

#### Validation Rules
- `user_id` path parameter must be provided and not empty
- `message` in request body must be provided and not empty after trimming
- `conversation_id` must be positive if provided
- Message length must be between 1 and 10000 characters

---

### GET /api/{user_id}/conversations
Retrieve a list of user's conversations.

#### Request
- **Method**: GET
- **Path**: `/api/{user_id}/conversations`
- **Path Parameters**:
  - `user_id` (string): The ID of the requesting user
- **Headers**:
  - `Authorization`: Bearer token (if required)

#### Response
- **Success Response (200 OK)**:
  ```json
  [
    {
      "id": 123,
      "title": "Add buy milk",
      "created_at": "2025-12-28T10:00:00Z",
      "updated_at": "2025-12-28T10:05:00Z",
      "message_count": 5
    },
    {
      "id": 122,
      "title": "Complete project tasks",
      "created_at": "2025-12-27T15:30:00Z",
      "updated_at": "2025-12-27T16:45:00Z",
      "message_count": 12
    }
  ]
  ```
- **Response Schema**:
  - Array of conversation objects with id, title, timestamps, and message count

- **Error Responses**:
  - `401 Unauthorized`: Invalid or missing authentication
  - `500 Internal Server Error`: Server error processing the request

#### Validation Rules
- `user_id` path parameter must be provided and not empty

---

### GET /api/{user_id}/conversations/{conversation_id}/messages
Retrieve the message history for a specific conversation.

#### Request
- **Method**: GET
- **Path**: `/api/{user_id}/conversations/{conversation_id}/messages`
- **Path Parameters**:
  - `user_id` (string): The ID of the requesting user
  - `conversation_id` (integer): The ID of the conversation
- **Headers**:
  - `Authorization`: Bearer token (if required)

#### Response
- **Success Response (200 OK)**:
  ```json
  [
    {
      "id": 456,
      "role": "user",
      "content": "Add buy milk to my tasks",
      "created_at": "2025-12-28T10:00:00Z",
      "tool_calls": null
    },
    {
      "id": 457,
      "role": "assistant",
      "content": "I've added 'buy milk' to your task list!",
      "created_at": "2025-12-28T10:00:05Z",
      "tool_calls": [
        {
          "tool_name": "add_task",
          "arguments": {
            "user_id": "user123",
            "title": "buy milk"
          },
          "result": {
            "task_id": 789,
            "status": "created"
          }
        }
      ]
    }
  ]
  ```
- **Response Schema**:
  - Array of message objects with id, role, content, timestamp, and optional tool calls

- **Error Responses**:
  - `401 Unauthorized`: Invalid or missing authentication
  - `404 Not Found`: Conversation does not exist or does not belong to user
  - `500 Internal Server Error`: Server error processing the request

#### Validation Rules
- `user_id` path parameter must be provided and not empty
- `conversation_id` path parameter must be provided and positive

---

## Common Error Response Format
All error responses follow this format:

```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": {
    "field": "field_name",
    "value": "invalid_value"
  }
}
```

## Error Codes
- `INVALID_INPUT`: Request data is invalid
- `AUTHENTICATION_FAILED`: Authentication credentials are invalid
- `AUTHORIZATION_FAILED`: User is not authorized for this action
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `RATE_LIMIT_EXCEEDED`: Request rate limit has been exceeded
- `INTERNAL_ERROR`: Server error occurred
- `SERVICE_UNAVAILABLE`: Service is temporarily unavailable