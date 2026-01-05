# Implementation Plan: Todo AI Chatbot Implementation Fixes

## Technical Context

This plan addresses critical issues in the Todo AI Chatbot Phase III implementation. The current codebase has multiple technical challenges that need to be resolved:

1. **Import Errors**: The backend fails to start due to import path inconsistencies and missing functions
2. **MCP Integration**: AI agent is not properly connected to MCP tools
3. **AI Provider Mismatch**: Current implementation uses Google Gemini instead of OpenAI as specified
4. **Frontend Components**: Missing chat interface components
5. **Architecture**: Need to ensure proper stateless architecture with database persistence

**Technology Stack**:
- Backend: Python FastAPI
- Database: SQLModel with PostgreSQL
- AI Framework: OpenAI Agents SDK (to be implemented)
- MCP Server: Official MCP SDK
- Frontend: OpenAI ChatKit
- Authentication: Better Auth

**Project Structure**:
- `/backend` - FastAPI application
- `/backend/src` - Source code with modules for api, services, models, database, mcp
- `/frontend` - React application with ChatKit integration
- `/specs` - Feature specifications

## Project Structure

The project follows a modular architecture:

```
backend/
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── chat_router.py
│   │       ├── conversation_router.py
│   │       └── mcp_router.py
│   ├── services/
│   │   ├── ai_agent_service.py
│   │   ├── conversation_service.py
│   │   └── mcp_service.py
│   ├── models/
│   │   ├── chat_models.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   └── mcp_tool.py
│   ├── database/
│   │   ├── session.py
│   │   └── engine.py
│   ├── mcp/
│   │   ├── server.py
│   │   └── tools/
│   └── main.py
frontend/
├── src/
│   ├── components/
│   ├── services/
│   └── app/
└── package.json
```

## Constitution Check

Based on the project constitution (template), this implementation will follow:

- **Test-First Approach**: All changes will include appropriate tests
- **Integration Testing**: Focus on inter-service communication between AI agent and MCP tools
- **Observability**: Proper logging and error handling throughout
- **Simplicity**: Start with minimal viable implementation and build from there

## Phase 0: Research & Resolution of Unknowns

### Research Task 1: Import Path Standardization
**Decision**: Standardize all imports to use consistent `src` package structure
**Rationale**: Current mixed import paths (`backend.src` vs `src`) cause resolution errors
**Approach**: Update all import paths to use relative imports from the `src` directory

### Research Task 2: Missing Function Implementation
**Decision**: Implement `get_db_session` function in database session module
**Rationale**: Multiple files import this function but it doesn't exist
**Approach**: Create proper async context manager with error handling

### Research Task 3: AI Provider Selection
**Decision**: Implement OpenAI Agents SDK as specified in original requirements
**Rationale**: Specification calls for OpenAI, not Google Gemini
**Alternatives considered**:
- Keep Google Gemini (easier short-term but violates spec)
- Use OpenAI (compliant with spec, requires more work)

### Research Task 4: MCP Tool Integration Pattern
**Decision**: Use OpenAI functions format for MCP tools integration
**Rationale**: OpenAI Agents SDK uses function calling for tool integration
**Approach**: Convert existing MCP tools to OpenAI-compatible function schemas

## Phase 1: Design & Architecture

### Data Model Design
Based on the specification, the following entities are defined:

**Task Entity**:
- user_id: String (foreign key to user)
- id: Integer (primary key, auto-increment)
- title: String (required task title)
- description: String (optional task details)
- completed: Boolean (completion status, default: false)
- created_at: DateTime (timestamp)
- updated_at: DateTime (timestamp)

**Conversation Entity**:
- id: Integer (primary key, auto-increment)
- user_id: String (foreign key to user)
- title: String (optional, auto-generated from first message)
- created_at: DateTime (timestamp)
- updated_at: DateTime (timestamp)

**Message Entity**:
- id: Integer (primary key, auto-increment)
- conversation_id: Integer (foreign key to conversation)
- user_id: String (foreign key to user)
- role: Enum (user, assistant)
- content: String (message content)
- tool_calls: JSON (optional, records of tools called by assistant)
- created_at: DateTime (timestamp)

### API Contract Design

**Chat Endpoint**:
- Method: POST
- Path: `/api/{user_id}/chat`
- Request: `{ "conversation_id": int, "message": string }`
- Response: `{ "conversation_id": int, "response": string, "tool_calls": array }`

**MCP Tools Endpoints**:
- GET `/api/v1/mcp/tools` - List available tools
- POST `/api/v1/mcp/tools/{tool_name}` - Execute specific tool

**Conversation Endpoints**:
- GET `/api/v1/conversations` - List user conversations
- GET `/api/v1/conversations/{id}` - Get specific conversation
- GET `/api/v1/conversations/{id}/messages` - Get conversation messages

## Phase 2: Implementation Approach

### Approach 1: Sequential Fix Implementation
**Order**:
1. Fix import errors and missing functions
2. Update AI agent to use OpenAI SDK
3. Connect MCP tools to AI agent
4. Implement frontend chat components

**Rationale**: Addresses blocking issues first, ensures stable foundation

### Approach 2: Parallel Component Development
**Order**:
- Backend fixes in parallel with frontend development
- MCP integration while updating AI provider

**Rationale**: Faster completion but higher risk of integration issues

**Selected Approach**: Sequential (Approach 1) - lower risk, more stable development

## Risk Analysis

### High Risks
- **Import Error Complexity**: Multiple files affected, could introduce new issues
- **AI Provider Switch**: Significant architectural change from Google to OpenAI
- **MCP Integration**: Complex connection between AI agent and tools

### Medium Risks
- **Database Migration**: Ensuring backward compatibility with existing data
- **Frontend Integration**: Connecting ChatKit with backend API

### Mitigation Strategies
- Thorough testing at each phase
- Maintain database backward compatibility
- Gradual rollout and validation

## Evaluation and Validation

### Definition of Done
- [ ] Backend starts without import errors
- [ ] All API endpoints accessible
- [ ] OpenAI integration working
- [ ] MCP tools properly connected to AI agent
- [ ] Frontend chat interface functional
- [ ] Natural language commands processed correctly
- [ ] All tests pass
- [ ] Error handling comprehensive

### Output Validation
- [ ] Format: All API responses follow specified contract
- [ ] Requirements: All functional requirements from spec implemented
- [ ] Safety: Proper input validation and error handling