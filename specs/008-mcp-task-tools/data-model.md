# Data Model: MCP Server with Task Management Tools

## Task Entity

**Description**: Represents a user's task with ID, title, description, completion status, and timestamps. This is the existing task model from the system that will be used by the MCP tools.

**Fields**:
- `id`: Primary key, auto-increment integer
- `user_id`: Foreign key to users table, string (indexed)
- `title`: Task title, string (required, max 255 chars)
- `description`: Task description, string (nullable, max 1000 chars)
- `completed`: Boolean indicating completion status (default: false)
- `created_at`: Timestamp when task was created (indexed, auto-default)
- `updated_at`: Timestamp when task was last updated (indexed, auto-updating)

**Relationships**:
- Many-to-one with User entity (many tasks to one user)
- No direct relationships needed for MCP tools

**Validation Rules**:
- `user_id` must reference an existing user
- `title` cannot be null or empty
- `user_id` cannot be null

## MCP Tool Input/Output Models

### AddTaskInput Model
**Description**: Input validation model for add_task tool

**Fields**:
- `user_id`: String (required) - Who owns this task
- `title`: String (required) - Task title
- `description`: String (optional) - Additional task details

### AddTaskOutput Model
**Description**: Output model for add_task tool

**Fields**:
- `task_id`: Integer - ID of created task
- `status`: String - Always "created"
- `title`: String - Echo back the title
- `description`: String or null - Echo back the description

### ListTasksInput Model
**Description**: Input validation model for list_tasks tool

**Fields**:
- `user_id`: String (required) - Whose tasks to retrieve
- `status`: String (optional) - Filter by "all", "pending", or "completed" (default: "all")

### ListTasksOutput Model
**Description**: Output model for list_tasks tool

**Fields**:
- `tasks`: Array of task objects containing id, title, description, completed, created_at, updated_at
- `count`: Integer - Total number of tasks returned

### CompleteTaskInput Model
**Description**: Input validation model for complete_task tool

**Fields**:
- `user_id`: String (required) - Who owns the task
- `task_id`: Integer (required) - Which task to complete

### CompleteTaskOutput Model
**Description**: Output model for complete_task tool

**Fields**:
- `task_id`: Integer - Echo back the task ID
- `status`: String - Always "completed"
- `title`: String - The task's title

### DeleteTaskInput Model
**Description**: Input validation model for delete_task tool

**Fields**:
- `user_id`: String (required) - Who owns the task
- `task_id`: Integer (required) - Which task to delete

### DeleteTaskOutput Model
**Description**: Output model for delete_task tool

**Fields**:
- `task_id`: Integer - Echo back the task ID
- `status`: String - Always "deleted"
- `title`: String - The deleted task's title

### UpdateTaskInput Model
**Description**: Input validation model for update_task tool

**Fields**:
- `user_id`: String (required) - Who owns the task
- `task_id`: Integer (required) - Which task to update
- `title`: String (optional) - New task title
- `description`: String (optional) - New task description

### UpdateTaskOutput Model
**Description**: Output model for update_task tool

**Fields**:
- `task_id`: Integer - Echo back the task ID
- `status`: String - Always "updated"
- `title`: String - The updated title
- `description`: String or null - The updated description

## State Transitions

**Task**:
- Created when add_task is called (completed=false)
- Updated when complete_task is called (completed=true)
- Updated when update_task is called (title/description changed)
- Deleted when delete_task is called (removed from system)

## Constraints and Indexes

**Tasks Table** (using existing structure):
- Primary Key: `id`
- Foreign Key: `user_id` → users.id
- Indexes: `user_id`, `completed`, `created_at`
- Check Constraints: None

## MCP Server Models

### MCPTool Model
**Description**: Represents a standardized interface for AI agents to interact with the task system

**Fields**:
- `name`: String - Tool name
- `description`: String - Tool description
- `input_schema`: JSON - JSON schema for tool inputs
- `output_schema`: JSON - JSON schema for tool outputs

**Methods**:
- `execute(input: dict) -> dict`: Execute the tool with given input

## API Access Patterns

**Common Queries**:
1. Get user's tasks by user_id with optional status filter
2. Create new task for a user
3. Update task completion status
4. Update task title/description
5. Delete specific task for user

**Performance Considerations**:
- Indexes on user_id and completed fields support efficient queries
- Created_at index supports sorting by creation time
- Foreign key constraints ensure data integrity