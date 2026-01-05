---
description: "Task list for Todo AI Chatbot - Chat API Endpoint implementation"
---

# Tasks: Todo AI Chatbot - Chat API Endpoint

**Input**: Design documents from `/specs/009-chat-api-endpoint/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The feature specification includes testing requirements (TR-001-TR-010), so test tasks are included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `backend/tests/`
- **Backend**: `backend/src/models/`, `backend/src/services/`, `backend/src/api/v1/`
- **Tests**: `backend/tests/unit/`, `backend/tests/integration/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend project structure per implementation plan in backend/
- [X] T002 Initialize Python project with FastAPI, SQLModel, Pydantic, Google AI SDK dependencies in backend/
- [X] T003 [P] Configure linting (flake8, black) and formatting tools in backend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup database schema and migrations framework using SQLModel in backend/src/database/
- [X] T005 [P] Create base models for Conversation and Message in backend/src/models/conversation.py and backend/src/models/message.py
- [X] T006 [P] Setup database connection pooling and session management in backend/src/database/
- [X] T007 Create base services for conversation operations in backend/src/services/conversation_service.py
- [X] T008 Configure error handling and logging infrastructure in backend/src/utils/
- [X] T009 Setup environment configuration management with proper secrets handling in backend/src/config/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Send Message and Receive AI Response (Priority: P1) 🎯 MVP

**Goal**: User can send a natural language message and receive an intelligent response to manage tasks through conversation.

**Independent Test**: Send a POST request to the chat endpoint with a simple message like "Hello" and verify a response is returned with proper conversation_id.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T010 [P] [US1] Contract test for POST /api/{user_id}/chat endpoint in backend/tests/contract/test_chat_api_contract.py
- [X] T011 [P] [US1] Integration test for basic message flow in backend/tests/integration/test_chat_api_basic_flow.py

### Implementation for User Story 1

- [X] T012 [P] [US1] Create AI agent service to handle Gemini API integration in backend/src/services/ai_agent_service.py
- [X] T013 [P] [US1] Create chat request/response Pydantic models in backend/src/models/chat_models.py
- [X] T014 [US1] Implement basic chat endpoint in backend/src/api/v1/chat_router.py (depends on T005, T007, T012)
- [X] T015 [US1] Add basic request validation and response formatting
- [X] T016 [US1] Implement conversation creation when no conversation_id provided
- [X] T017 [US1] Add logging for chat operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Stateless Request Processing (Priority: P1)

**Goal**: Chat endpoint is completely stateless so any server instance can handle any request, enabling horizontal scaling and resilience.

**Independent Test**: Start a conversation on one server instance, restart the server, and continue the conversation - the AI should maintain full context from database-stored history.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T018 [P] [US2] Integration test for server restart scenario in backend/tests/integration/test_stateless_processing.py
- [X] T019 [P] [US2] Test for no server-side session storage in backend/tests/unit/test_no_session_storage.py

### Implementation for User Story 2

- [X] T020 [P] [US2] Implement conversation history loading from database in backend/src/services/conversation_service.py (depends on T005, T007)
- [X] T021 [US2] Update chat endpoint to load full conversation history before AI processing in backend/src/api/v1/chat_router.py
- [X] T022 [US2] Remove any server-side session or memory storage of conversation state
- [X] T023 [US2] Add proper database queries to fetch conversation history ordered by created_at

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Conversation History Persistence (Priority: P2)

**Goal**: Every message and response is saved to the database so users can reference past interactions and the AI maintains context across sessions.

**Independent Test**: Have a multi-turn conversation, then query the database directly to verify all user and assistant messages are stored with correct timestamps and conversation_id.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T024 [P] [US3] Integration test for message persistence in backend/tests/integration/test_message_persistence.py
- [X] T025 [P] [US3] Unit test for message model validation in backend/tests/unit/test_message_model.py

### Implementation for User Story 3

- [X] T026 [P] [US3] Update Message model to properly handle role='user' and role='assistant' in backend/src/models/message.py
- [X] T027 [US3] Implement storing user messages in database before AI processing in backend/src/services/conversation_service.py
- [X] T028 [US3] Implement storing assistant responses in database after AI processing in backend/src/services/conversation_service.py
- [X] T029 [US3] Update conversation updated_at timestamp on each message interaction in backend/src/services/conversation_service.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - AI Agent Integration with MCP Tools (Priority: P1)

**Goal**: AI understands user intent and automatically calls appropriate MCP tools so users can manage tasks without knowing technical details.

**Independent Test**: Send commands like "Add buy groceries" and verify that the add_task MCP tool is called with correct parameters and the task appears in the database.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T030 [P] [US4] Integration test for MCP tool invocation in backend/tests/integration/test_mcp_tool_integration.py
- [X] T031 [P] [US4] Contract test for tool call recording in backend/tests/contract/test_tool_call_recording.py

### Implementation for User Story 4

- [X] T032 [P] [US4] Create ToolCall model for embedded JSONB in Message in backend/src/models/tool_call.py
- [X] T033 [US4] Update AI agent service to pass MCP tools configuration to Gemini API in backend/src/services/ai_agent_service.py
- [X] T034 [US4] Implement capturing and recording MCP tool calls in assistant messages in backend/src/services/ai_agent_service.py
- [X] T035 [US4] Update chat endpoint to handle tool calls in AI responses and return them in response format in backend/src/api/v1/chat_router.py

**Checkpoint**: User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Error Handling and Graceful Degradation (Priority: P2)

**Goal**: Clear error messages when something goes wrong so users understand what happened and can take appropriate action.

**Independent Test**: Simulate various failure scenarios (database down, invalid conversation_id, AI API failure) and verify appropriate error responses are returned.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T036 [P] [US5] Integration test for database unavailability in backend/tests/integration/test_database_error_handling.py
- [X] T037 [P] [US5] Integration test for invalid conversation_id in backend/tests/integration/test_invalid_conversation_handling.py
- [X] T038 [P] [US5] Integration test for AI API failures in backend/tests/integration/test_ai_api_error_handling.py

### Implementation for User Story 5

- [X] T039 [P] [US5] Create error response models in backend/src/models/error_models.py
- [X] T040 [US5] Implement validation for user_id existence in backend/src/api/v1/chat_router.py
- [X] T041 [US5] Implement validation for conversation_id existence and user ownership in backend/src/api/v1/chat_router.py
- [X] T042 [US5] Add proper error responses for all failure scenarios in backend/src/api/v1/chat_router.py
- [X] T043 [US5] Implement fallback handling for AI agent failures in backend/src/services/ai_agent_service.py

**Checkpoint**: All user stories should now be independently functional with proper error handling

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T044 [P] Documentation updates in backend/docs/
- [X] T045 Code cleanup and refactoring across all services
- [X] T046 Performance optimization for database queries to prevent N+1 problems
- [X] T047 [P] Additional unit tests in backend/tests/unit/
- [X] T048 Security hardening for user isolation and validation
- [X] T049 Run quickstart.md validation to ensure all components work together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with all previous stories but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /api/{user_id}/chat endpoint in backend/tests/contract/test_chat_api_contract.py"
Task: "Integration test for basic message flow in backend/tests/integration/test_chat_api_basic_flow.py"

# Launch all models for User Story 1 together:
Task: "Create AI agent service to handle Gemini API integration in backend/src/services/ai_agent_service.py"
Task: "Create chat request/response Pydantic models in backend/src/models/chat_models.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence