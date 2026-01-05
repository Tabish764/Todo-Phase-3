# Quickstart Guide: Fix AI Chatbot Integration Issues

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.12+ for backend development
- PostgreSQL database running
- Better Auth configured for authentication
- OpenAI API access for AI features
- @ai-sdk/react package installed in frontend

## Setup Instructions

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   # In backend/.env
   DATABASE_URL=postgresql://user:password@localhost:5432/chatbot_db
   BETTER_AUTH_SECRET=your-secret-key
   OPENAI_API_KEY=your-openai-api-key
   ```

3. **Run database migrations**:
   ```bash
   python -m backend.src.migrations.run
   ```

4. **Start the backend server**:
   ```bash
   python -m backend.src.main
   # Server will run on http://localhost:8000
   ```

### Frontend Setup

1. **Install Node dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables**:
   ```bash
   # In frontend/.env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
   ```

3. **Start the frontend development server**:
   ```bash
   npm run dev
   # Frontend will run on http://localhost:3000
   ```

## Running Tests

### Backend Tests
```bash
# Run all backend tests
cd backend
pytest

# Run specific test file
pytest tests/integration/test_chat_api.py
```

### Frontend Tests
```bash
# Run all frontend tests
cd frontend
npm test

# Run specific test
npm test -- src/components/Chat/ChatKitWrapper.test.tsx
```

## Key Endpoints

### Chat Endpoints
- `POST /api/{user_id}/chat` - Send message and receive AI response
- `GET /api/{user_id}/conversations` - Get user's conversation list
- `GET /api/{user_id}/conversations/{conversation_id}/messages` - Get conversation history

### Task Endpoints
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task

## Configuration

### Backend Configuration
- Update `backend/src/config.py` to configure database, authentication, and AI settings
- Update `backend/src/main.py` to register new API routers

### Frontend Configuration
- Update `frontend/src/services/chatService.ts` to configure API endpoints
- Update `frontend/src/hooks/useChat.ts` to configure chat behavior
- Update `frontend/src/components/Chat/ChatKitWrapper.tsx` to configure UI components

## Development Workflow

1. **Implement backend changes** in `backend/src/`
2. **Update API contracts** in `specs/001-fix-chat-integration/contracts/`
3. **Implement frontend changes** in `frontend/src/`
4. **Write/update tests** in `backend/tests/` and `frontend/tests/`
5. **Verify integration** by testing the full flow

## Troubleshooting

### Common Issues

**Chat endpoint returns 404**
- Verify the chat router is registered in `backend/src/main.py`
- Check that the prefix matches frontend expectations

**Tools not executing**
- Verify the ToolExecutionService is properly implemented
- Check that AI responses include proper tool call formats

**Navigation not visible**
- Verify the chat button is added to the main page component
- Check authentication requirements are properly handled

**API routes misaligned**
- Ensure frontend service calls match backend route patterns
- Verify user_id is properly passed in all requests