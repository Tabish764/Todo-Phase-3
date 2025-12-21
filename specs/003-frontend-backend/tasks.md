# Implementation Tasks: Frontend-Backend Integration

**Branch**: `003-frontend-backend` | **Date**: 2025-12-15 | **Plan**: [specs/003-frontend-backend/plan.md](specs/003-frontend-backend/plan.md)

**Note**: This template is filled in by the `/sp.tasks` command. See `.specify/templates/commands/tasks.md` for the execution workflow.

## Task Dependencies

- **Prerequisites**: Backend API must be running with `/tasks` endpoints (GET, POST, PUT, DELETE)
- **Parallel Development**: Frontend API service can be developed independently of UI updates
- **Integration Point**: UI components connect to API service through hooks

## Test Strategy

### Unit Tests
- [ ] API service methods (getTasks, createTask, updateTask, deleteTask) with mock responses
- [ ] Error handling in API service for different HTTP status codes
- [ ] Hook logic for state management and API calls

### Integration Tests
- [ ] End-to-end flow from UI to backend API and back
- [ ] Network error handling and retry logic
- [ ] Loading state management during API calls

### Acceptance Tests
- [ ] All scenarios from spec.md pass with real backend API
- [ ] User can create, read, update, delete tasks via API
- [ ] Error states are properly handled and displayed

## Tasks

### Phase 1: API Service Layer

#### Task 1.1: Create API Service Module
- **Objective**: Implement API service to communicate with backend
- **Files**: `frontend/src/services/api.ts`
- **Acceptance**:
  - Service can make GET, POST, PUT, DELETE requests to backend API
  - Proper error handling for different HTTP status codes
  - Configurable base URL with fallback to localhost:8000
  - TypeScript interfaces matching backend API schema

#### Task 1.2: Implement Get Tasks Functionality
- **Objective**: Fetch tasks from backend API instead of local storage
- **Files**: `frontend/src/services/api.ts`, `frontend/src/hooks/useTaskManager.ts`
- **Acceptance**:
  - API service can fetch all tasks from `/tasks` endpoint
  - Loading state is properly managed during API call
  - Error state is handled when API call fails
  - Returns array of Task objects matching schema

#### Task 1.3: Implement Create Task Functionality
- **Objective**: Create new tasks via backend API
- **Files**: `frontend/src/services/api.ts`, `frontend/src/hooks/useTaskManager.ts`
- **Acceptance**:
  - API service can create new task via POST to `/tasks` endpoint
  - Returns created Task object with server-generated ID and timestamps
  - Proper validation of input data before sending to backend
  - Error handling for validation failures

#### Task 1.4: Implement Update Task Functionality
- **Objective**: Update existing tasks via backend API
- **Files**: `frontend/src/services/api.ts`, `frontend/src/hooks/useTaskManager.ts`
- **Acceptance**:
  - API service can update task via PUT to `/tasks/{id}` endpoint
  - Returns updated Task object with correct timestamps
  - Handles partial updates (only sending changed fields)
  - Error handling for not-found scenarios

#### Task 1.5: Implement Delete Task Functionality
- **Objective**: Delete tasks via backend API
- **Files**: `frontend/src/services/api.ts`, `frontend/src/hooks/useTaskManager.ts`
- **Acceptance**:
  - API service can delete task via DELETE to `/tasks/{id}` endpoint
  - Returns success confirmation or error
  - Handles not-found scenarios appropriately
  - 204 No Content response is handled properly

### Phase 2: Frontend Integration

#### Task 2.1: Update useTaskManager Hook
- **Objective**: Replace local storage with API service calls
- **Files**: `frontend/src/hooks/useTaskManager.ts`
- **Acceptance**:
  - Initial tasks are loaded from backend API instead of local storage
  - createTask function calls backend API
  - updateTask function calls backend API
  - deleteTask function calls backend API
  - toggleTaskCompletion function calls backend API
  - Loading states are properly managed during API calls
  - Error states are handled appropriately

#### Task 2.2: Add Loading State Management
- **Objective**: Show loading indicators during API operations
- **Files**: `frontend/src/hooks/useTaskManager.ts`, `frontend/src/components/TaskForm/TaskForm.tsx`, `frontend/src/components/TaskItem/TaskItem.tsx`
- **Acceptance**:
  - Individual task operations show loading states
  - Form submission shows loading state
  - UI prevents duplicate submissions during loading
  - Loading states are cleared appropriately on success/error

#### Task 2.3: Add Error Handling and Display
- **Objective**: Show user-friendly error messages when API calls fail
- **Files**: `frontend/src/hooks/useTaskManager.ts`, `frontend/src/components/TaskForm/TaskForm.tsx`, `frontend/src/components/TaskItem/TaskItem.tsx`
- **Acceptance**:
  - Network errors are caught and displayed appropriately
  - Validation errors from backend are shown to users
  - Error messages are clear and actionable
  - UI recovers gracefully from API failures

### Phase 3: Testing and Validation

#### Task 3.1: Unit Test API Service
- **Objective**: Test all API service methods with mock responses
- **Files**: `frontend/src/services/api.test.ts`
- **Acceptance**:
  - All HTTP methods are tested with success and error scenarios
  - Error handling is verified for different HTTP status codes
  - Network timeout scenarios are tested
  - All TypeScript interfaces work as expected

#### Task 3.2: Unit Test Updated Hook
- **Objective**: Test the updated useTaskManager hook with mocked API service
- **Files**: `frontend/src/hooks/useTaskManager.test.ts`
- **Acceptance**:
  - All hook functions work with mocked API responses
  - Loading and error states are properly managed
  - State transitions occur correctly during API operations
  - Error recovery scenarios are handled

#### Task 3.3: End-to-End Testing
- **Objective**: Test complete user flows with real backend API
- **Files**: Integration tests in `frontend/tests/e2e/`
- **Acceptance**:
  - User can complete all CRUD operations via API
  - Data persists between page refreshes
  - Error scenarios are handled gracefully
  - All acceptance scenarios from spec.md pass

## Implementation Order

1. Phase 1 (API Service Layer) - Can be developed in parallel with backend testing
2. Phase 2 (Frontend Integration) - Depends on Phase 1 completion
3. Phase 3 (Testing and Validation) - Can begin during Phase 2 but final validation after Phase 2

## Success Criteria

- [ ] All tasks from backend are displayed in frontend on initial load
- [ ] New tasks created in frontend are stored on backend
- [ ] Task updates in frontend are persisted to backend
- [ ] Task deletions in frontend are removed from backend
- [ ] Loading states provide feedback during API operations
- [ ] Error messages are displayed when API calls fail
- [ ] All acceptance scenarios from spec.md pass
- [ ] Unit tests have >80% coverage for new code