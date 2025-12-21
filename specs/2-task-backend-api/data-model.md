# Data Model: Task Backend API (Frontend Integration Only)

## Task Entity

**Description**: Represents a user's task with title, description, and completion status

**Fields**:
- `id`: string (UUID) - Unique identifier for the task (generated automatically)
- `title`: string (required, 1-200 characters) - The task title
- `description`: string (optional) - Additional details about the task
- `completed`: boolean - Indicates if the task is completed (default: false)
- `created_at`: ISO timestamp - Timestamp of when the task was created
- `updated_at`: ISO timestamp - Timestamp of when the task was last updated

**Validation Rules**:
- `title` must be 1-200 characters
- `title` is required (cannot be empty)
- `completed` defaults to false when creating a new task
- `created_at` is set automatically when creating a task
- `updated_at` is updated automatically when modifying a task

**State Transitions**:
- New task: `completed = false` → `completed = true` (when user marks as complete)
- Completed task: `completed = true` → `completed = false` (when user marks as incomplete)

## In-Memory Storage Structure

**Data Structure**: Python dictionary with UUID string as key and Task object as value

```python
# Example structure:
{
    "task_uuid_1": {
        "id": "task_uuid_1",
        "title": "Sample task",
        "description": "Sample description",
        "completed": False,
        "created_at": "2025-12-15T10:30:00Z",
        "updated_at": "2025-12-15T10:30:00Z"
    },
    "task_uuid_2": {
        "id": "task_uuid_2",
        "title": "Another task",
        "description": "Another description",
        "completed": True,
        "created_at": "2025-12-15T10:31:00Z",
        "updated_at": "2025-12-15T10:32:00Z"
    }
}
```

**Operations**:
- CREATE: Add new task to dictionary with generated UUID
- READ: Retrieve task from dictionary by ID
- UPDATE: Modify existing task in dictionary
- DELETE: Remove task from dictionary by ID

## API Request/Response Models

### Create Task Request
```json
{
  "title": "string (required, 1-200 characters)",
  "description": "string (optional)"
}
```

### Update Task Request
```json
{
  "title": "string (optional, 1-200 characters)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

### Task Response (All Endpoints)
```json
{
  "id": "string (UUID)",
  "title": "string",
  "description": "string (optional)",
  "completed": "boolean",
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp"
}
```

### Error Response
```json
{
  "error": "string (human readable message)"
}
```

### List Tasks Response
```json
[
  {
    "id": "string (UUID)",
    "title": "string",
    "description": "string (optional)",
    "completed": "boolean",
    "created_at": "ISO timestamp",
    "updated_at": "ISO timestamp"
  }
]
```