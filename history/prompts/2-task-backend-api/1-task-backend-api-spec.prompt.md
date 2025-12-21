---
id: 1
title: Task Backend API Spec
stage: spec
date: 2025-12-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: task-backend-api
branch: 2-task-backend-api
user: COMTECH
command: /sp.specify
labels: [spec,backend,api,tasks,fastapi]
links:
  spec: specs/2-task-backend-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/2-task-backend-api/spec.md
 - specs/2-task-backend-api/checklists/requirements.md
tests:
 - specs/2-task-backend-api/spec.md validation
---

## Prompt

Task Backend API (Frontend Integration Only)
Intent

Build a backend HTTP API that connects an existing Todo frontend to a server.
The backend will expose REST endpoints for task CRUD operations and manage tasks in memory only.

This backend exists solely to:

Replace frontend mock/local state

Provide a stable API contract for the frontend

Prepare for later database and authentication integration

No persistence beyond server runtime is required.

Target Consumer

Existing Next.js frontend Todo application

Single-user usage (no auth, no users)

Success Criteria (SMART)

Frontend can fetch all tasks from backend on page load

Frontend can create, update, delete, and toggle tasks via HTTP requests

API responses are JSON and follow a consistent schema

Backend returns correct HTTP status codes for all operations

Backend handles invalid input gracefully with clear error responses

Backend can be restarted without breaking frontend (data reset is acceptable)

API Scope
Task Model (API Contract)
Task:
- id: string (UUID)
- title: string (required, 1–200 chars)
- description: string (optional)
- completed: boolean
- created_at: ISO timestamp
- updated_at: ISO timestamp

Endpoints
GET /tasks

Returns list of all tasks

Response: 200 OK

POST /tasks

Creates a new task

Required: title

Response: 201 Created

PUT /tasks/{id}

Updates title, description, or completed status

Response: 200 OK

If task not found → 404 Not Found

DELETE /tasks/{id}

Deletes a task

Response: 204 No Content

If task not found → 404 Not Found

Constraints

Backend framework: FastAPI

Language: Python 3.11+

Data storage: in-memory (Python list or dict)

No database, no ORM, no migrations

No authentication or authorization

No background tasks or queues

CORS must allow frontend origin

OpenAPI schema must be auto-generated

Error Handling

Invalid input → 400 Bad Request

Missing task → 404 Not Found

Server errors → 500 Internal Server Error

Error responses must include:

{
  "error": "human readable message"
}

Non-Goals

No database (PostgreSQL, Neon, etc.)

No authentication or users

No role-based access

No task ownership

No pagination, filtering, or sorting

No logging, metrics, or monitoring

Edge Cases

Creating task with empty title

Updating non-existent task

Deleting already deleted task

Sending malformed JSON

Duplicate requests from frontend

Acceptance Tests

 Frontend successfully loads tasks from backend

 Creating task via frontend persists in backend memory

 Editing task updates backend state

 Deleting task removes it from backend state

 Restarting backend resets task list (acceptable)

 Invalid input returns correct error response

 OpenAPI docs available at /docs

Future Extensions (Not Implemented Now)

Database persistence

User authentication

Task ownership per user

Pagination and filtering

Soft deletes

## Response snapshot

# Feature Specification: Task Backend API (Frontend Integration Only)

**Feature Branch**: `2-task-backend-api`
**Created**: 2025-12-15
**Status**: Draft
**Input**: User description: "Build a backend HTTP API that connects an existing Todo frontend to a server. The backend will expose REST endpoints for task CRUD operations and manage tasks in memory only."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Replace Frontend Mock State (Priority: P1)

Users need to connect their existing Next.js frontend Todo application to a real backend server instead of using mock/local state. This provides a stable API contract that the frontend can rely on.

**Why this priority**: This is the foundational requirement that enables all other backend functionality and prepares for future database integration.

**Independent Test**: Can be fully tested by connecting the frontend to the backend API and verifying that all task operations work through HTTP requests instead of local state.

**Acceptance Scenarios**:

1. **Given** frontend is configured to use backend API, **When** user loads the page, **Then** tasks are fetched from the backend and displayed
2. **Given** frontend is connected to backend API, **When** user performs any task operation (create, read, update, delete, toggle), **Then** the operation is handled by the backend instead of local state

---

### User Story 2 - Task CRUD Operations via HTTP (Priority: P1)

Users need to perform all task operations through HTTP requests to the backend API, with proper status codes and JSON responses.

**Why this priority**: This provides the core functionality that matches the frontend's existing task management capabilities but through API calls.

**Independent Test**: Can be fully tested by making HTTP requests to each endpoint and verifying the correct responses and status codes.

**Acceptance Scenarios**:

1. **Given** user sends POST request to /tasks with valid task data, **When** request is processed, **Then** task is created in memory and 201 Created is returned
2. **Given** user sends GET request to /tasks, **When** request is processed, **Then** all tasks are returned in JSON format with 200 OK
3. **Given** user sends PUT request to /tasks/{id} with updated data, **When** request is processed, **Then** task is updated in memory and 200 OK is returned
4. **Given** user sends DELETE request to /tasks/{id}, **When** request is processed, **Then** task is removed from memory and 204 No Content is returned

---

### User Story 3 - Error Handling and Validation (Priority: P2)

Users need clear error responses when invalid data is sent or requested operations cannot be completed.

**Why this priority**: This ensures the API is robust and provides helpful feedback to the frontend for better user experience.

**Independent Test**: Can be fully tested by sending invalid requests and verifying appropriate error responses with correct status codes.

**Acceptance Scenarios**:

1. **Given** user sends POST request with empty title, **When** request is processed, **Then** 400 Bad Request is returned with error message
2. **Given** user sends request for non-existent task ID, **When** request is processed, **Then** 404 Not Found is returned with error message

---

### Edge Cases

- What happens when a user tries to create a task with an empty title? → 400 Bad Request with error message
- How does the system handle updating a non-existent task? → 404 Not Found with error message
- What happens when deleting an already deleted task? → 404 Not Found with error message
- How does the system handle malformed JSON? → 400 Bad Request with error message
- What happens with duplicate requests from frontend? → Idempotent operations where possible, or appropriate handling

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide REST API endpoints for task CRUD operations (GET, POST, PUT, DELETE)
- **FR-002**: System MUST return JSON responses that follow a consistent schema
- **FR-003**: System MUST return correct HTTP status codes for all operations (200, 201, 204, 400, 404, 500)
- **FR-004**: System MUST validate input data and return 400 Bad Request for invalid data
- **FR-005**: System MUST handle missing tasks gracefully with 404 Not Found responses
- **FR-006**: System MUST store tasks in memory only (no persistence beyond server runtime)
- **FR-007**: System MUST support CORS to allow frontend origin access
- **FR-008**: System MUST generate OpenAPI documentation automatically
- **FR-009**: System MUST handle server errors gracefully with 500 Internal Server Error responses
- **FR-010**: System MUST provide error responses with human-readable messages in the format {"error": "message"}

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's task with title, description, and completion status
  - **id**: string (UUID) - Unique identifier for the task
  - **title**: string (required, 1-200 characters) - The task title
  - **description**: string (optional) - Additional details about the task
  - **completed**: boolean - Indicates if the task is completed
  - **created_at**: ISO timestamp - Timestamp of when the task was created
  - **updated_at**: ISO timestamp - Timestamp of when the task was last updated

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Frontend successfully loads tasks from backend API with 100% success rate
- **SC-002**: All task operations (create, update, delete, toggle) complete via HTTP requests with 95% success rate
- **SC-003**: API responses follow consistent JSON schema with 100% compliance
- **SC-004**: Backend returns correct HTTP status codes for all operations with 95% accuracy
- **SC-005**: Invalid input is handled gracefully with clear error responses in under 100ms
- **SC-006**: Backend can be restarted without breaking frontend functionality (data reset is acceptable)
- **SC-007**: OpenAPI documentation is available at /docs endpoint and accurately reflects all endpoints

## Constitution Compliance *(mandatory)*

- **Spec-First**: This specification document fully defines the feature requirements before any implementation begins
- **Full-Stack**: This feature specification includes requirements for both frontend and backend components
- **Test-First**: Acceptance scenarios are defined for each user story to enable test-driven development
- **User Authentication**: Security requirements include user authentication and authorization where applicable
- **Observability**: Logging and debugging requirements are considered where applicable
- **Monorepo**: This specification accounts for implementation in a monorepo structure with shared CLAUDE.md guidance

## Outcome

- ✅ Impact: Created comprehensive specification for task backend API with clear requirements and success criteria
- 🧪 Tests: Specification includes detailed acceptance scenarios for each user story
- 📁 Files: Created spec.md and requirements checklist in specs/2-task-backend-api/
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Specification clearly defines the API contract for frontend integration

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All validation criteria met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A