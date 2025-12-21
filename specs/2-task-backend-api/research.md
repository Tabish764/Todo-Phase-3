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