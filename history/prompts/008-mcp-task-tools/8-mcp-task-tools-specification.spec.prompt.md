---
id: 8
title: MCP Task Tools Specification
stage: spec
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: mcp-task-tools
branch: 008-mcp-task-tools
user: Claude
command: /sp.specify
labels: [specification, mcp, task-management, ai-tools]
links:
  spec: specs/008-mcp-task-tools/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/008-mcp-task-tools/spec.md
  - specs/008-mcp-task-tools/checklists/requirements.md
tests:
  - spec quality checklist completed
---

## Prompt

## Feature 2: MCP Server with Task Management Tools

### What to Build
An MCP server that exposes 5 standardized tools for AI agents to interact with the task management system. Each tool must be stateless and operate directly on the database.

### Tool 1: add_task

**Purpose:** Create a new task for the user

**Required Input:**
- user_id (string) - Who owns this task
- title (string) - Task title

**Optional Input:**
- description (string) - Additional task details

**Expected Output:**
- task_id (integer) - ID of created task
- status (string) - Always "created"
- title (string) - Echo back the title
- description (string or null) - Echo back the description

**Behavior:**
- Insert new task record into database
- Set completed=false by default
- Set created_at and updated_at to current timestamp
- Return task details immediately after creation

**Error Handling:**
- If user_id missing: Return error "User ID is required"
- If title missing: Return error "Task title is required"
- If database error: Return error with details

---

### Tool 2: list_tasks

**Purpose:** Retrieve tasks with optional filtering by completion status

**Required Input:**
- user_id (string) - Whose tasks to retrieve

**Optional Input:**
- status (string) - Filter by "all", "pending", or "completed" (default: "all")

**Expected Output:**
- tasks (array) - List of task objects, each containing:
  - id (integer)
  - title (string)
  - description (string or null)
  - completed (boolean)
  - created_at (ISO datetime string)
  - updated_at (ISO datetime string)
- count (integer) - Total number of tasks returned

**Filtering Logic:**
- "all" - Return all tasks for user
- "pending" - Return only tasks where completed=false
- "completed" - Return only tasks where completed=true

**Sorting:**
- Order by created_at descending (newest first)

**Error Handling:**
- If user_id missing: Return error "User ID is required"
- If database error: Return error with details

---

### Tool 3: complete_task

**Purpose:** Mark a specific task as completed

**Required Input:**
- user_id (string) - Who owns the task
- task_id (integer) - Which task to complete

**Expected Output:**
- task_id (integer) - Echo back the task ID
- status (string) - Always "completed"
- title (string) - The task's title

**Behavior:**
- Query database for task with given task_id
- Verify task belongs to user_id
- Update completed=true
- Update updated_at to current timestamp
- Return task details

**Error Handling:**
- If task not found: Return error "Task not found"
- If task belongs to different user: Return error "Unauthorized"
- If task already completed: Return error "Task is already completed"

---

### Tool 4: delete_task

**Purpose:** Permanently remove a task from the database

**Required Input:**
- user_id (string) - Who owns the task
- task_id (integer) - Which task to delete

**Expected Output:**
- task_id (integer) - Echo back the task ID
- status (string) - Always "deleted"
- title (string) - The deleted task's title

**Behavior:**
- Query database for task with given task_id
- Verify task belongs to user_id
- Delete task record from database
- Return confirmation with task details

**Error Handling:**
- If task not found: Return error "Task not found"
- If task belongs to different user: Return error "Unauthorized"

---

### Tool 5: update_task

**Purpose:** Modify a task's title or description

**Required Input:**
- user_id (string) - Who owns the task
- task_id (integer) - Which task to update

**Optional Input (at least one required):**
- title (string) - New task title
- description (string) - New task description

**Expected Output:**
- task_id (integer) - Echo back the task ID
- status (string) - Always "updated"
- title (string) - The updated title
- description (string or null) - The updated description

**Behavior:**
- Query database for task with given task_id
- Verify task belongs to user_id
- Update only the fields provided in input
- Update updated_at to current timestamp
- Return updated task details

**Error Handling:**
- If task not found: Return error "Task not found"
- If task belongs to different user: Return error "Unauthorized"
- If neither title nor description provided: Return error "Nothing to update"

---

### MCP Server Requirements

**Discoverability:**
- Server must list all 5 tools when queried
- Each tool must include name, description, and JSON schema for inputs

**Validation:**
- Validate all inputs against defined schemas before execution
- Return clear error messages for invalid inputs

**Statelessness:**
- No in-memory state between requests
- All data persists to database immediately
- Server can restart without losing data

**Authorization:**
- Every tool must verify user_id matches task ownership
- Prevent users from accessing other users' tasks

---

## Response snapshot

Created a comprehensive feature specification for the MCP Server with Task Management Tools. The specification includes:

1. Created a new feature branch `008-mcp-task-tools`
2. Created the specification file `specs/008-mcp-task-tools/spec.md` with:
   - User scenarios and testing (3 prioritized user stories)
   - Functional requirements (12 specific requirements)
   - Key entities definitions
   - Success criteria with measurable outcomes
   - Edge cases consideration

3. Created a quality checklist at `specs/008-mcp-task-tools/checklists/requirements.md` to validate the specification

The specification covers all 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) with proper input/output definitions, error handling, and authorization requirements. It defines the MCP server requirements for discoverability, validation, statelessness, and authorization.

## Outcome

- ✅ Impact: Created complete feature specification for MCP Task Management Tools
- 🧪 Tests: Spec quality checklist completed and validated
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase (/sp.plan)
- 🧠 Reflection: Specification addresses all requirements from user input with proper user scenarios, functional requirements, and success criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase