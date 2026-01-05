# Quickstart: Todo AI Chatbot - Chat API Endpoint

## Prerequisites
- Python 3.12
- PostgreSQL database
- Google AI API key for Gemini
- MCP Server running with task tools

## Setup

1. **Environment Setup**:
   ```bash
   # Install dependencies
   pip install fastapi sqlmodel pydantic google-generativeai python-multipart

   # Set environment variables
   export DATABASE_URL="postgresql://user:password@localhost/dbname"
   export GOOGLE_AI_API_KEY="your-api-key-here"
   export MCP_SERVER_URL="http://localhost:3000"
   ```

2. **Database Initialization**:
   ```bash
   # Run database migrations to create conversations and messages tables
   # (Assuming migration scripts exist from feature 007)
   python -m backend.src.migrations.init
   ```

3. **Start the Service**:
   ```bash
   # Start the FastAPI application
   uvicorn backend.src.main:app --host 0.0.0.0 --port 8000

   # Or with reload for development
   uvicorn backend.src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Usage

### Start a New Conversation
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, I want to add a task"
  }'
```

### Continue an Existing Conversation
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 123,
    "message": "Show me my tasks"
  }'
```

### Expected Response
```json
{
  "conversation_id": 123,
  "response": "I've added your task to the list!",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "arguments": {
        "user_id": "user123",
        "title": "Sample task"
      },
      "result": {
        "task_id": 5,
        "status": "created",
        "title": "Sample task"
      }
    }
  ]
}
```

## Development

1. **Run Tests**:
   ```bash
   # Unit tests
   pytest tests/unit/

   # Integration tests
   pytest tests/integration/
   ```

2. **API Documentation**:
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## Architecture Notes

- The endpoint is stateless - all conversation history is loaded from the database on each request
- User authentication/authorization is handled by the path parameter (user_id)
- MCP tools are called synchronously during AI processing
- All messages are persisted before and after AI processing