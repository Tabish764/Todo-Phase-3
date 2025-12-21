# Implementation Tasks: Neon Database Integration

**Branch**: `004-neon-database` | **Date**: 2025-12-16 | **Plan**: [specs/004-neon-database/plan.md](specs/004-neon-database/plan.md)

**Note**: This template is filled in by the `/sp.tasks` command. See `.specify/templates/commands/tasks.md` for the execution workflow.

## Task Dependencies

- **Prerequisites**: Neon database instance created and connection string available
- **Parallel Development**: Database models can be developed independently of API integration
- **Integration Point**: API endpoints connect to database layer instead of in-memory storage

## Test Strategy

### Unit Tests
- [ ] Database model validation and constraints
- [ ] Repository/service layer functions
- [ ] Database connection and session management
- [ ] Error handling for database operations

### Integration Tests
- [ ] End-to-end flow from API to database and back
- [ ] Database transaction handling
- [ ] Connection pooling behavior
- [ ] Migration scripts execution

### Acceptance Tests
- [ ] All scenarios from spec.md pass with database backend
- [ ] User can create, read, update, delete tasks via database
- [ ] Data persists across application restarts
- [ ] Error states are properly handled and displayed

## Tasks

### Phase 1: Database Setup

#### Task 1.1: Add Database Dependencies
- **Objective**: Install required packages for PostgreSQL and SQLModel integration
- **Files**: `backend/requirements.txt`, `backend/pyproject.toml`
- **Acceptance**:
  - SQLModel, asyncpg, and alembic are added to dependencies
  - Dependencies can be installed successfully with uv
  - No conflicts with existing dependencies
- [X] **Status**: Completed

#### Task 1.2: Create Database Connection Module
- **Objective**: Implement database connection and session management
- **Files**: `backend/src/database/connection.py`, `backend/src/database/session.py`
- **Acceptance**:
  - Database connection string is read from environment variables
  - Connection pooling is configured appropriately
  - Session management follows best practices
  - Connection errors are handled gracefully
- [X] **Status**: Completed

#### Task 1.3: Set up Alembic for Migrations
- **Objective**: Configure Alembic for database schema management
- **Files**: `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/versions/`
- **Acceptance**:
  - Alembic is configured to work with SQLModel
  - Initial migration can be generated and applied
  - Migration commands work correctly
  - Database schema can be version controlled
- [X] **Status**: Completed

### Phase 2: Data Models

#### Task 2.1: Create SQLModel Task Model
- **Objective**: Define Task model using SQLModel with database-specific configurations
- **Files**: `backend/src/database/models.py`
- **Acceptance**:
  - Task model inherits from SQLModel and includes table configuration
  - All required fields are defined with proper types and constraints
  - Validation rules match requirements from spec
  - Created/updated timestamps are handled automatically
- [X] **Status**: Completed

#### Task 2.2: Update Existing Models
- **Objective**: Ensure existing Pydantic schemas remain compatible with SQLModel
- **Files**: `backend/src/models/task.py`, `backend/src/schemas/task.py`
- **Acceptance**:
  - Existing API schemas remain unchanged
  - SQLModel models can be converted to/from API schemas
  - Validation behavior remains consistent
  - No breaking changes to API contracts
- [X] **Status**: Completed

### Phase 3: Data Access Layer

#### Task 3.1: Create Task Repository
- **Objective**: Implement data access layer for task operations
- **Files**: `backend/src/database/repositories.py` or `backend/src/database/task_crud.py`
- **Acceptance**:
  - Create task function works with database
  - Read tasks function retrieves from database
  - Update task function modifies database records
  - Delete task function removes from database
  - All operations include proper error handling
- [X] **Status**: Completed

#### Task 3.2: Update In-Memory DB Implementation
- **Objective**: Replace in-memory database with database repository
- **Files**: `backend/src/database/memory_db.py`
- **Acceptance**:
  - In-memory implementation is replaced with database calls
  - All existing functionality is preserved
  - Database operations are used instead of in-memory storage
  - Error handling is consistent with previous behavior
- [X] **Status**: Completed

### Phase 4: API Integration

#### Task 4.1: Update Task Endpoints
- **Objective**: Connect API endpoints to database repository
- **Files**: `backend/src/api/v1/endpoints/tasks.py`
- **Acceptance**:
  - GET /tasks retrieves from database
  - POST /tasks creates in database
  - PUT /tasks/{id} updates in database
  - DELETE /tasks/{id} removes from database
  - Response format remains unchanged
- [X] **Status**: Completed

#### Task 4.2: Update Main Application
- **Objective**: Initialize database connection in main application
- **Files**: `backend/src/main.py`
- **Acceptance**:
  - Database connection is established on startup
  - Database tables are created if they don't exist
  - Application can handle database connection failures gracefully
  - Health check endpoint verifies database connectivity
- [X] **Status**: Completed

### Phase 5: Testing and Validation

#### Task 5.1: Unit Tests for Database Layer
- **Objective**: Test database models and repository functions
- **Files**: `backend/tests/unit/test_database.py`, `backend/tests/unit/test_models.py`
- **Acceptance**:
  - All database model validation is tested
  - Repository functions are tested with mocked database
  - Error conditions are properly tested
  - Test coverage is >80% for database layer
- [X] **Status**: Completed

#### Task 5.2: Integration Tests
- **Objective**: Test end-to-end functionality with real database
- **Files**: `backend/tests/integration/test_tasks_api.py`
- **Acceptance**:
  - All CRUD operations work with real database
  - Data persists across requests
  - API responses match expected format
  - Error handling works correctly
- [X] **Status**: Completed

#### Task 5.3: End-to-End Testing
- **Objective**: Test complete user flows with database backend
- **Files**: Integration tests in `backend/tests/e2e/`
- **Acceptance**:
  - User can complete all CRUD operations via API with database storage
  - Data persists between application restarts
  - All acceptance scenarios from spec.md pass
  - Frontend integration continues to work without changes
- [X] **Status**: Completed

## Implementation Order

1. Phase 1 (Database Setup) - Foundation layer
2. Phase 2 (Data Models) - Depends on Phase 1 completion
3. Phase 3 (Data Access Layer) - Depends on Phases 1 & 2
4. Phase 4 (API Integration) - Depends on previous phases
5. Phase 5 (Testing and Validation) - Can be done in parallel with Phase 4

## Success Criteria

- [ ] Database connection is established successfully
- [ ] All existing API endpoints work with database storage
- [ ] Data persists across application restarts
- [ ] All existing frontend functionality continues to work
- [ ] Database migrations work correctly
- [ ] Error handling is appropriate for database failures
- [ ] All acceptance scenarios from spec.md pass
- [ ] Unit tests have >80% coverage for new code