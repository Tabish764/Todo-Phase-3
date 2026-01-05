# Todo AI Chatbot Implementation Fixes - Specification

## Feature Overview

This feature addresses critical issues in the Todo AI Chatbot Phase III implementation. The current codebase has import errors preventing startup, incomplete MCP integration, and an AI provider mismatch (Google Gemini vs OpenAI as specified). This specification outlines the fixes needed to align the implementation with the original requirements.

## User Scenarios & Testing

### Primary User Flow
1. User accesses the Todo AI Chatbot frontend
2. User starts a conversation with natural language commands like "Add a task to buy groceries"
3. AI agent processes the command and calls appropriate MCP tools
4. Tools execute against the database to manage tasks
5. AI returns natural language response confirming actions
6. Conversation history persists in database and remains accessible

### Secondary Flows
- User can list existing tasks with commands like "Show me my tasks"
- User can complete tasks with commands like "Mark task 1 as complete"
- User can update or delete tasks with natural language commands
- User can resume conversations after server restarts

### Error Scenarios
- Handle invalid API keys gracefully
- Handle database connection failures
- Handle malformed user commands
- Handle tool execution failures

## Functional Requirements

### FR-001: Backend Startup
**Requirement**: The backend application must start successfully without import errors
**Acceptance Criteria**:
- `uv run uvicorn src.main:app --reload` command executes without import errors
- All API endpoints are accessible
- Database connection is established successfully

### FR-002: Import Path Standardization
**Requirement**: All import paths must follow a consistent `src` package structure
**Acceptance Criteria**:
- All files use consistent import paths without mixed `backend.src` and `src` references
- Import paths match actual file locations
- No import resolution errors occur

### FR-003: Missing Function Implementation
**Requirement**: Missing `get_db_session` function must be implemented
**Acceptance Criteria**:
- `src/database/session.py` contains `get_db_session` function
- Function provides proper async context management
- Function includes error handling and session cleanup

### FR-004: MCP Tool Integration
**Requirement**: AI agent must properly integrate with MCP tools
**Acceptance Criteria**:
- AI agent can call all 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- Tool call results are properly executed and returned
- Tool calls are properly formatted and handled

### FR-005: Chat Endpoint MCP Configuration
**Requirement**: Chat endpoint must use actual MCP server instead of placeholder configuration
**Acceptance Criteria**:
- `/api/{user_id}/chat` endpoint connects to real MCP server
- Tool calls from AI are properly executed against MCP tools
- Response includes actual tool call results

### FR-006: OpenAI Integration
**Requirement**: Replace Google Gemini with OpenAI Agents SDK as specified
**Acceptance Criteria**:
- AI agent service uses OpenAI SDK instead of Google Gemini
- MCP tools work as OpenAI functions
- Natural language processing uses OpenAI models

### FR-007: Frontend Chat Interface
**Requirement**: Implement chat interface components using OpenAI ChatKit
**Acceptance Criteria**:
- Chat interface communicates with backend chat API
- Conversation history is displayed properly
- Real-time chat functionality works

### FR-008: Database Persistence
**Requirement**: Conversation state must persist in database
**Acceptance Criteria**:
- All conversation history saved to database
- Messages properly associated with conversations
- User isolation maintained

### FR-009: Natural Language Processing
**Requirement**: AI must process natural language commands correctly
**Acceptance Criteria**:
- Commands like "Add a task" trigger add_task MCP tool
- Commands like "Show my tasks" trigger list_tasks MCP tool
- Appropriate responses returned for all supported commands

### FR-010: Error Handling
**Requirement**: Comprehensive error handling throughout the system
**Acceptance Criteria**:
- Invalid user inputs handled gracefully
- Database errors don't crash the system
- API errors return appropriate HTTP status codes

## Success Criteria

### Performance Metrics
- Backend starts within 10 seconds
- API endpoints respond within 2 seconds under normal load
- Natural language commands processed within 5 seconds
- Tool calls execute within 1 second

### Quality Metrics
- 95% of natural language commands correctly interpreted and processed
- 100% of API endpoints accessible after fixes
- 0 import errors in the codebase
- All 5 MCP tools function correctly with AI agent

### User Experience Metrics
- Users can successfully manage tasks through natural language
- Conversation history persists across sessions
- Error messages are user-friendly and informative
- Response times are acceptable for chat interactions

## Key Entities

### Task Entity
- user_id: String (identifies the user who owns the task)
- id: Integer (unique identifier for the task)
- title: String (task description)
- description: String (optional detailed description)
- completed: Boolean (completion status)
- created_at: Timestamp (when task was created)
- updated_at: Timestamp (when task was last modified)

### Conversation Entity
- user_id: String (identifies the user who owns the conversation)
- id: Integer (unique identifier for the conversation)
- created_at: Timestamp (when conversation was started)
- updated_at: Timestamp (when conversation was last active)
- title: String (optional conversation title)

### Message Entity
- id: Integer (unique identifier for the message)
- conversation_id: Integer (foreign key to conversation)
- user_id: String (identifies the user who sent the message)
- role: Enum (user or assistant)
- content: String (message content)
- tool_calls: JSON (optional tool calls made by assistant)
- created_at: Timestamp (when message was created)

## Assumptions

1. OpenAI API keys will be properly configured in the environment
2. Database connection parameters are correctly set in configuration
3. Frontend will be deployed to a domain that can be added to OpenAI's domain allowlist
4. Users have valid authentication tokens for API access
5. Network connectivity exists between services and external APIs

## Dependencies

1. OpenAI SDK for Python
2. FastAPI framework
3. SQLModel for database operations
4. Neon PostgreSQL database
5. Better Auth for user authentication
6. OpenAI ChatKit for frontend components

## Constraints

1. Must maintain backward compatibility with existing database schema
2. Must preserve existing API contracts where possible
3. Must follow stateless architecture principles
4. Must maintain user data isolation
5. Must handle concurrent users appropriately