# API Contract: Task Backend API (Frontend Integration Only)

## Base URL
`http://localhost:8000` (development) or configured server URL

## Common Headers
- `Content-Type: application/json`
- `Accept: application/json`

## Endpoints

### GET /tasks
**Description**: Retrieve all tasks from the backend

**Authentication**: None required

**Request Parameters**: None

**Response**:
- Status: `200 OK`
- Body: Array of Task objects

**Example Request**:
```
GET /tasks
```

**Example Response**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Sample task",
    "description": "Sample description",
    "completed": false,
    "created_at": "2025-12-15T10:30:00Z",
    "updated_at": "2025-12-15T10:30:00Z"
  }
]
```

### POST /tasks
**Description**: Create a new task

**Authentication**: None required

**Request Body**:
```json
{
  "title": "string (required, 1-200 characters)",
  "description": "string (optional)"
}
```

**Response**:
- Status: `201 Created`
- Body: Created Task object

**Example Request**:
```
POST /tasks
Content-Type: application/json

{
  "title": "New task",
  "description": "Task description"
}
```

**Example Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "created_at": "2025-12-15T10:31:00Z",
  "updated_at": "2025-12-15T10:31:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input (empty title, title too long, etc.)
```json
{
  "error": "Title is required and must be between 1 and 200 characters"
}
```

### PUT /tasks/{id}
**Description**: Update an existing task

**Authentication**: None required

**Path Parameter**:
- `id`: Task UUID string

**Request Body**:
```json
{
  "title": "string (optional, 1-200 characters)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

**Response**:
- Status: `200 OK`
- Body: Updated Task object

**Example Request**:
```
PUT /tasks/550e8400-e29b-41d4-a716-446655440001
Content-Type: application/json

{
  "title": "Updated task title",
  "completed": true
}
```

**Example Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "Updated task title",
  "description": "Task description",
  "completed": true,
  "created_at": "2025-12-15T10:31:00Z",
  "updated_at": "2025-12-15T10:32:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input
```json
{
  "error": "Title must be between 1 and 200 characters"
}
```
- `404 Not Found`: Task with given ID does not exist
```json
{
  "error": "Task not found"
}
```

### DELETE /tasks/{id}
**Description**: Delete an existing task

**Authentication**: None required

**Path Parameter**:
- `id`: Task UUID string

**Response**:
- Status: `204 No Content`
- Body: Empty

**Example Request**:
```
DELETE /tasks/550e8400-e29b-41d4-a716-446655440001
```

**Error Responses**:
- `404 Not Found`: Task with given ID does not exist
```json
{
  "error": "Task not found"
}
```

## Common Error Responses

### 400 Bad Request
```json
{
  "error": "Human-readable error message explaining the validation issue"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "An internal server error occurred"
}
```

## Data Validation Rules

- Task title: Required, 1-200 characters
- Task description: Optional, any length
- Task completed: Boolean (true/false)
- ID: UUID string format
- Timestamps: ISO 8601 format