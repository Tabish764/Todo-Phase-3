# Data Model: Optimistic Updates for Task Operations

## Task Entity

### Fields
- **id**: string - Unique identifier for the task (UUID format)
  - Server-generated for successful operations
  - Temporary UUID for optimistic updates
- **title**: string - Task title (1-200 characters)
- **description**: string (optional) - Task description (up to 1000 characters)
- **completed**: boolean - Completion status of the task
- **createdAt**: Date - Timestamp when task was created
- **updatedAt**: Date - Timestamp when task was last updated
- **pending**: boolean (frontend only) - Indicates operation in progress
- **tempId**: string (frontend only) - Temporary UUID before server assigns real ID

### Relationships
- No direct relationships with other entities

### Validation Rules
- Title must be 1-200 characters
- Description must be ≤ 1000 characters if provided
- Completed must be boolean
- createdAt and updatedAt must be valid date objects

### State Transitions
- `pending=true` → `pending=false` when API call completes successfully
- `pending=true` → task removal when API call fails (for create/delete operations)
- `completed=false` → `completed=true` when task is marked complete
- `completed=true` → `completed=false` when task is marked incomplete

## API Response Structure

### Task Response
```typescript
interface TaskResponse {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string; // ISO date string from API
  updatedAt: string; // ISO date string from API
}
```

### Optimistic Task Extension (Frontend)
```typescript
interface OptimisticTask extends TaskResponse {
  pending?: boolean;
  tempId?: string;
}
```

## API Request Structure

### Create Task Request
```typescript
interface CreateTaskRequest {
  title: string;
  description?: string;
  completed: boolean; // defaults to false
}
```

### Update Task Request
```typescript
interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}
```

## State Management

### Frontend State
The useTaskManager hook will maintain:
- `tasks: OptimisticTask[]` - Array of tasks including those in pending state
- `loading: boolean` - Overall loading state
- `error: string | null` - Error messages

### Pending Operations
- Create: Task added with temporary ID and pending=true
- Delete: Task removed from list immediately, restored if API fails
- Update: Task property updated immediately, reverted if API fails