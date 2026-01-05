# Quickstart: Todo AI Chatbot Implementation Fixes

## Overview
Quickstart guide for setting up and running the fixed Todo AI Chatbot application with proper import paths, MCP integration, and OpenAI alignment.

## Prerequisites
- Python 3.12+ and pip
- Node.js 18+ and npm/yarn/pnpm
- Access to OpenAI API (for OpenAI Agents SDK)
- PostgreSQL database (or Neon Serverless PostgreSQL)
- Git for version control
- uv package manager (or pip)

## Setup Instructions

### 1. Clone and Navigate
```bash
# Clone the repository (if needed)
git clone <repository-url>
cd <project-root>

# Navigate to the project directory
cd hackathon-II-phase-II
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies using uv
uv venv  # Create virtual environment
source .venv/bin/activate  # Activate virtual environment (Linux/Mac)
# On Windows: .venv\Scripts\activate

uv pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_chatbot
NEON_DATABASE_URL=your_neon_connection_string  # If using Neon

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=info

# Better Auth Configuration (if applicable)
BETTER_AUTH_SECRET=your_auth_secret
BETTER_AUTH_URL=http://localhost:8000
```

### 4. Database Setup
```bash
# Run database migrations (if using alembic)
cd backend
source .venv/bin/activate
alembic upgrade head

# Or create tables directly with SQLModel
python -c "from src.database.engine import engine; from src.models.conversation import Conversation, Message; from src.models.task import Task; import asyncio; from sqlmodel import SQLModel; async def create_tables(): async with engine.begin() as conn: await conn.run_sync(SQLModel.metadata.create_all); asyncio.run(create_tables())"
```

### 5. Project Structure
After setup, the project should have this structure:

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
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── app/
│   └── package.json
└── specs/
    └── 012-fix-chatbot-issues/
```

### 6. Backend Startup
```bash
# From backend directory
cd backend
source .venv/bin/activate

# Run the development server
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
echo "NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_domain_key" >> .env.local

# Run the development server
npm run dev
```

## Key Integration Points

### Backend API Endpoints
- `POST /api/{user_id}/chat` - Send messages and receive AI responses with tool calls
- `GET /api/{user_id}/conversations` - Get user's conversation list
- `GET /api/{user_id}/conversations/{conversation_id}/messages` - Get conversation history
- `GET /api/v1/mcp/tools` - Get available MCP tools
- `POST /api/v1/mcp/tools/{tool_name}` - Execute specific MCP tool

### OpenAI Integration
- AI agent service uses OpenAI Agents SDK
- MCP tools registered as OpenAI functions
- Proper function calling for tool execution
- Response formatting for frontend consumption

### Database Integration
- SQLModel for database operations
- Async PostgreSQL sessions
- Conversation and message persistence
- Task management with user isolation

## Running Tests
```bash
# Backend tests
cd backend
source .venv/bin/activate
pytest

# Frontend tests
cd frontend
npm test
```

## Common Issues and Solutions

### Issue: Import Errors
**Solution**: Verify all import paths follow the `src` package structure. Run the import fix scripts to standardize paths.

### Issue: OpenAI API Connection
**Solution**: Verify OPENAI_API_KEY is correctly set in environment variables and has proper permissions.

### Issue: Database Connection
**Solution**: Check DATABASE_URL configuration and ensure PostgreSQL is running and accessible.

### Issue: MCP Tools Not Working
**Solution**: Verify MCP server is properly initialized and tools are registered with the AI agent.

## Next Steps
1. Verify backend starts without import errors
2. Test MCP tool integration with AI agent
3. Implement frontend chat components
4. Test end-to-end conversation flow
5. Validate natural language command processing
6. Perform comprehensive testing