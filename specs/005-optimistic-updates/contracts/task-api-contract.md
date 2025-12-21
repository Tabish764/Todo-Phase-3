# API Contract: Task Operations with Optimistic Updates

## Overview
This contract defines the API endpoints for task operations. The optimistic updates are implemented on the frontend, so the backend API endpoints remain unchanged. The contract ensures compatibility with the optimistic update pattern.

## Base Path
`/api/v1`

## Endpoints

### GET /tasks
**Description**: Retrieve all tasks for the authenticated user
**Authentication**: Required (JWT token)

**Response**:
- Status: 200 OK
- Content-Type: application/json
- Body: Array of Task objects

```json
[
  {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description (optional)",
    "completed": false,
    "created_at": "2025-12-17T10:00:00Z",
    "updated_at": "2025-12-17T10:00:00Z"
  }
]
```

### POST /tasks
**Description**: Create a new task
**Authentication**: Required (JWT token)

**Request Body**:
```json
{
  "title": "Task title (required)",
  "description": "Task description (optional)",
  "completed": false
}
```

**Response**:
- Status: 201 Created
- Content-Type: application/json
- Body: Created Task object

```json
{
  "id": "new-uuid-string",
  "title": "Task title",
  "description": "Task description (optional)",
  "completed": false,
  "created_at": "2025-12-17T10:00:00Z",
  "updated_at": "2025-12-17T10:00:00Z"
}
```

### PUT /tasks/{id}
**Description**: Update an existing task
**Authentication**: Required (JWT token)

**Path Parameters**:
- id: Task UUID

**Request Body** (all fields optional):
```json
{
  "title": "Updated title (optional)",
  "description": "Updated description (optional)",
  "completed": true
}
```

**Response**:
- Status: 200 OK
- Content-Type: application/json
- Body: Updated Task object

```json
{
  "id": "uuid-string",
  "title": "Updated title",
  "description": "Updated description (optional)",
  "completed": true,
  "created_at": "2025-12-17T10:00:00Z",
  "updated_at": "2025-12-17T11:00:00Z"
}
```

### DELETE /tasks/{id}
**Description**: Delete a task
**Authentication**: Required (JWT token)

**Path Parameters**:
- id: Task UUID

**Response**:
- Status: 204 No Content

## Error Responses
All endpoints may return:
- 400 Bad Request: Invalid input data
- 401 Unauthorized: Missing or invalid JWT token
- 404 Not Found: Task with specified ID does not exist
- 500 Internal Server Error: Server error

```json
{
  "error": "Error message"
}
```

## Frontend Implementation Notes

### Optimistic Update Pattern
The frontend will implement optimistic updates for better UX:

1. **Task Creation**:
   - Generate temporary ID
   - Add task to UI with pending state
   - Call POST /tasks
   - On success: Update with server ID and remove pending state
   - On failure: Remove task from UI and show error

2. **Task Deletion**:
   - Remove task from UI immediately
   - Call DELETE /tasks/{id}
   - On success: Keep task removed
   - On failure: Add task back to UI and show error

3. **Task Update**:
   - Update UI immediately
   - Call PUT /tasks/{id}
   - On success: Keep updated state
   - On failure: Revert to previous state and show error

## Data Consistency
- The backend ensures data integrity and persistence
- The frontend handles temporary UI state
- If API calls fail, the frontend reverts to the last known good state