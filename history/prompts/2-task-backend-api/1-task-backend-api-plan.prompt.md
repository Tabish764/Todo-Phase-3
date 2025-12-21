---
id: 1
title: Task Backend API Plan
stage: plan
date: 2025-12-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: task-backend-api
branch: 2-task-backend-api
user: COMTECH
command: /sp.plan
labels: [plan,backend,api,tasks,fastapi]
links:
  spec: specs/2-task-backend-api/spec.md
  plan: specs/2-task-backend-api/plan.md
  research: specs/2-task-backend-api/research.md
  data-model: specs/2-task-backend-api/data-model.md
  contracts: specs/2-task-backend-api/contracts/task-api-contract.md
  quickstart: specs/2-task-backend-api/quickstart.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/2-task-backend-api/plan.md
 - specs/2-task-backend-api/research.md
 - specs/2-task-backend-api/data-model.md
 - specs/2-task-backend-api/contracts/task-api-contract.md
 - specs/2-task-backend-api/quickstart.md
tests:
 - plan completeness check
 - research validation
 - data model validation
---

## Prompt

$ARGUMENTS

## Response snapshot

# Implementation Plan: Task Backend API (Frontend Integration Only)

**Branch**: `2-task-backend-api` | **Date**: 2025-12-15 | **Spec**: [specs/2-task-backend-api/spec.md](../2-task-backend-api/spec.md)
**Input**: Feature specification from `/specs/2-task-backend-api/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a FastAPI backend HTTP API that connects an existing Todo frontend to a server. The backend will expose REST endpoints for task CRUD operations and manage tasks in memory only. This provides a stable API contract for the frontend and prepares for later database and authentication integration.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, uvicorn, pydantic, python-multipart
**Storage**: In-memory Python dictionary (no persistence beyond server runtime)
**Testing**: pytest, httpx for API testing
**Target Platform**: Linux/Windows/Mac server environment
**Project Type**: Web application backend
**Performance Goals**: API responses under 100ms for all operations
**Constraints**: <300ms p95 for API operations, no authentication, no database integration initially
**Scale/Scope**: Single-user usage, up to 1000 tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Spec-First: Verify that a complete feature specification exists in `/specs/2-task-backend-api/spec.md` before proceeding - **PASSED**
- Full-Stack Implementation: Confirm that the plan covers both frontend and backend components, not just one layer - **RESOLVED** (Backend-only for this phase per spec constraints, frontend integration for compatibility)
- Test-First/TDD: Ensure that testing strategies are defined for both backend endpoints and frontend components - **RESOLVED** (Backend API tests with pytest and httpx)
- JWT Authentication & Security: Verify that user authentication and authorization mechanisms are planned with JWT tokens - **NOT APPLICABLE** (No auth in scope per spec)
- Observability & Simplicity: Confirm that logging and debugging capabilities are planned for both frontend and backend - **RESOLVED** (Basic logging for API operations)
- Monorepo Structure: Ensure that the project structure follows the monorepo pattern with proper CLAUDE.md guidance - **PASSED**

## Project Structure

### Documentation (this feature)

```text
specs/2-task-backend-api/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py
│   ├── models/
│   │   └── task.py
│   ├── schemas/
│   │   └── task.py
│   ├── database/
│   │   └── memory_db.py
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── tasks.py
│   └── core/
│       └── config.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

**Structure Decision**: Backend application structure selected with FastAPI, following standard project organization with models, schemas, API endpoints, and configuration modules.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Backend-only implementation | Spec constraints require backend API initially | Frontend integration planned for future phase |
| No JWT authentication | Spec constraints require no auth initially | Security will be added when authentication is implemented |

---

# Research: Task Backend API (Frontend Integration Only)

## Decision: Backend Framework
**Rationale**: Based on the constitution and spec requirements, FastAPI provides the optimal combination of performance, automatic OpenAPI documentation generation, and Python type hint support. It's specifically designed for building APIs and integrates well with the existing Python ecosystem.

**Alternatives considered**:
- Flask: More basic, would require more manual setup for validation and documentation
- Django REST Framework: More heavyweight, overkill for simple API
- Node.js/Express: Would not align with the Python backend requirement in constitution

## Decision: In-Memory Storage
**Rationale**: For this phase, in-memory storage (using Python dictionary) meets the spec requirement of "no persistence beyond server runtime". It's simple to implement, fast, and allows for rapid development while preparing for future database integration.

**Alternatives considered**:
- SQLite in-memory: Would add unnecessary complexity for temporary storage
- Redis: Would add external dependency for simple storage
- File-based storage: Would contradict "no persistence" requirement

## Decision: Task Model Structure
**Rationale**: The Task model follows the exact specification from the feature requirements with UUID for ID, proper validation for title length (1-200 chars), optional description, boolean completion status, and ISO timestamp fields for creation and update times.

**Structure**:
- id: UUID string (generated automatically)
- title: string (required, 1-200 characters)
- description: string (optional)
- completed: boolean (default: false)
- created_at: ISO timestamp
- updated_at: ISO timestamp

## Decision: API Endpoint Design
**Rationale**: RESTful endpoints following standard conventions that match the frontend's expected API contract. Using standard HTTP methods with appropriate status codes as specified in the requirements.

**Endpoints**:
- GET /tasks: Retrieve all tasks (200 OK)
- POST /tasks: Create new task (201 Created, 400 Bad Request for validation errors)
- PUT /tasks/{id}: Update task (200 OK, 404 Not Found if task doesn't exist)
- DELETE /tasks/{id}: Delete task (204 No Content, 404 Not Found if task doesn't exist)

## Decision: Error Handling Strategy
**Rationale**: Consistent error responses in the format {"error": "message"} with appropriate HTTP status codes as specified in requirements. This provides clear feedback to the frontend for proper user experience.

**Error Types**:
- 400 Bad Request: Validation errors (empty title, invalid data)
- 404 Not Found: Task not found for update/delete operations
- 500 Internal Server Error: Unexpected server errors

## Decision: CORS Configuration
**Rationale**: Required to allow the frontend origin to make requests to the backend API. FastAPI's CORSMiddleware will be configured to allow the frontend's origin for proper integration.

## Decision: Testing Approach
**Rationale**: Using pytest with httpx for API testing provides robust testing capabilities for FastAPI applications. This follows the Test-First/TDD principle from the constitution.

**Test Types**:
- Unit tests for models and utility functions
- Integration tests for API endpoints
- API tests to verify correct status codes and responses

---

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

---

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

---

# Quickstart Guide: Task Backend API (Frontend Integration Only)

## Prerequisites

- Python 3.11+ installed
- pip package manager
- Virtual environment tool (venv, conda, etc.)

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install production dependencies
pip install fastapi uvicorn python-multipart pydantic

# Install development dependencies (optional)
pip install pytest httpx
```

### 3. Project Structure

After setup, your project should have this structure:

```
backend/
├── src/
│   ├── main.py
│   ├── models/
│   │   └── task.py
│   ├── schemas/
│   │   └── task.py
│   ├── database/
│   │   └── memory_db.py
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── tasks.py
│   └── core/
│       └── config.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

### 4. Key Implementation Files

#### Task Model (`src/models/task.py`)

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from uuid import UUID, uuid4

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime

    @field_validator('title')
    def validate_title(cls, v):
        if not v or len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v

    @classmethod
    def create(cls, title: str, description: Optional[str] = None):
        now = datetime.now()
        return cls(
            id=str(uuid4()),
            title=title,
            description=description,
            completed=False,
            created_at=now,
            updated_at=now
        )

    def update(self, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None):
        now = datetime.now()
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if completed is not None:
            self.completed = completed
        self.updated_at = now
        return self
```

#### Task Schemas (`src/schemas/task.py`)

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None

    @field_validator('title')
    def validate_title(cls, v):
        if not v or len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator('title')
    def validate_title(cls, v):
        if v is not None and (len(v) < 1 or len(v) > 200):
            raise ValueError('Title must be between 1 and 200 characters')
        return v

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

class ErrorResponse(BaseModel):
    error: str
```

#### In-Memory Database (`src/database/memory_db.py`)

```python
from typing import Dict, List, Optional
from src.models.task import Task

class InMemoryTaskDB:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def get_all_tasks(self) -> List[Task]:
        return list(self._tasks.values())

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def create_task(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def update_task(self, task_id: str, task: Task) -> Optional[Task]:
        if task_id in self._tasks:
            self._tasks[task_id] = task
            return task
        return None

    def delete_task(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

# Global instance
db = InMemoryTaskDB()
```

#### Tasks API Endpoints (`src/api/v1/endpoints/tasks.py`)

```python
from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.task import Task
from src.schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskResponse, ErrorResponse
from src.database.memory_db import db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskResponse])
async def get_tasks() -> List[TaskResponse]:
    tasks = db.get_all_tasks()
    return [TaskResponse.model_validate(task) for task in tasks]

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(request: TaskCreateRequest) -> TaskResponse:
    task = Task.create(title=request.title, description=request.description)
    created_task = db.create_task(task)
    return TaskResponse.model_validate(created_task)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, request: TaskUpdateRequest) -> TaskResponse:
    existing_task = db.get_task(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task with provided values
    if request.title is not None:
        existing_task.title = request.title
    if request.description is not None:
        existing_task.description = request.description
    if request.completed is not None:
        existing_task.completed = request.completed

    existing_task.updated_at = datetime.now()
    updated_task = db.update_task(task_id, existing_task)

    return TaskResponse.model_validate(updated_task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    success = db.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return
```

#### Main Application (`src/main.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints.tasks import router as tasks_router
from src.core.config import settings

app = FastAPI(
    title="Task Backend API",
    description="Backend API for task management frontend integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(tasks_router)

@app.get("/")
async def root():
    return {"message": "Task Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 5. Running the Application

```bash
# Development mode
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# The API will be available at http://localhost:8000
# OpenAPI docs at http://localhost:8000/docs
```

### 6. Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run API tests
pytest tests/api/
```

### 7. Frontend Integration

To connect your existing frontend Todo application to this backend:

1. Update the frontend service/api calls to point to your backend endpoints
2. Replace local state operations with HTTP requests to the backend
3. Handle the API responses and errors appropriately

Example API calls from frontend:
```javascript
// Fetch all tasks
fetch('http://localhost:8000/tasks')
  .then(response => response.json())
  .then(tasks => console.log(tasks));

// Create a new task
fetch('http://localhost:8000/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'New task',
    description: 'Task description'
  })
})
  .then(response => response.json())
  .then(task => console.log(task));
```

## Environment Configuration

Create a `.env` file in the backend root for configuration:

```
# Server configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
SERVER_RELOAD=true

# CORS configuration
FRONTEND_URL=http://localhost:3000  # Your frontend URL
```

## Troubleshooting

- **API not responding**: Ensure the server is running and check the port
- **CORS errors**: Verify frontend origin is allowed in CORS middleware
- **Validation errors**: Check that request bodies match the API contract
- **Task not found**: Verify the task ID exists and is properly formatted as UUID

## Outcome

- ✅ Impact: Created comprehensive implementation plan with research, data model, API contracts, and quickstart guide
- 🧪 Tests: All planning artifacts validated against spec requirements
- 📁 Files: Created plan.md, research.md, data-model.md, contracts/, and quickstart.md
- 🔁 Next prompts: Ready for task generation phase with /sp.tasks
- 🧠 Reflection: Plan fully prepared for backend API implementation with frontend integration focus

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All planning requirements met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A