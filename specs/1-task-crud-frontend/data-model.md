# Data Model: Task CRUD Frontend

## Task Entity

**Description**: Represents a user's task with title, description, and completion status

**Fields**:
- `id`: string - Unique identifier for the task (generated as UUID or timestamp-based ID)
- `title`: string (required, 1-200 characters) - The task title
- `description`: string (optional) - Additional details about the task
- `completed`: boolean - Indicates if the task is completed (default: false)
- `createdAt`: Date - Timestamp of when the task was created
- `updatedAt`: Date - Timestamp of when the task was last updated

**Validation Rules**:
- `title` must be 1-200 characters
- `title` is required (cannot be empty)
- `completed` defaults to false when creating a new task
- `createdAt` is set automatically when creating a task
- `updatedAt` is updated automatically when modifying a task

**State Transitions**:
- New task: `completed = false` → `completed = true` (when user marks as complete)
- Completed task: `completed = true` → `completed = false` (when user marks as incomplete)

## State Management Structure

**In-Memory State** (managed by React state):
```typescript
interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}
```

**Task Operations**:
- CREATE: Add new task to tasks array
- READ: Display tasks from tasks array
- UPDATE: Modify existing task in tasks array
- DELETE: Remove task from tasks array
- TOGGLE: Update completion status of task in tasks array

## Local Storage Schema

**Persistence Format**:
```typescript
interface PersistedData {
  tasks: Task[];
  lastUpdated: Date;
}
```

**Storage Key**: `task-manager-data`

**Persistence Strategy**:
- Save to localStorage after each task operation
- Load from localStorage on app initialization
- Optional persistence (if localStorage is available)