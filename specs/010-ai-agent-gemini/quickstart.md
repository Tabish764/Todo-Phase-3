# Quickstart: Todo AI Chatbot - AI Agent Configuration (OpenAI Agents SDK with Gemini API)

## Prerequisites
- Python 3.12
- Google Gemini API key
- MCP Server with all 5 tools (add_task, list_tasks, complete_task, delete_task, update_task)
- Chat API Endpoint running (Feature 009)

## Setup

1. **Install Dependencies**:
   ```bash
   pip install google-generativeai python-dotenv
   ```

2. **Configure Environment Variables**:
   ```bash
   # Add to .env file
   GOOGLE_GEMINI_API_KEY=your-api-key-here
   GEMINI_MODEL_NAME=gemini-pro  # or gemini-1.5-pro
   ```

3. **Initialize the Agent**:
   ```python
   from backend.src.agents.gemini_agent import GeminiAgent

   agent = GeminiAgent.from_config()
   ```

## API Usage

### Basic Task Creation
```python
response = agent.process_message(
    user_id="user123",
    message="Add a task to buy groceries",
    conversation_history=[]
)

print(response.content)  # "I've added 'Buy groceries' to your task list!"
print(response.tool_calls)  # [{"tool_name": "add_task", "arguments": {...}, "result": {...}}]
```

### Task Listing
```python
response = agent.process_message(
    user_id="user123",
    message="Show me my tasks",
    conversation_history=[]
)

print(response.content)  # "Here are your pending tasks: [...]"
```

### Multi-turn Conversation
```python
# First message establishes context
response1 = agent.process_message(
    user_id="user123",
    message="I need to remember to call the doctor",
    conversation_history=[]
)

# Second message refers to previous context
response2 = agent.process_message(
    user_id="user123",
    message="Mark that task as done",
    conversation_history=[
        {"role": "user", "content": "I need to remember to call the doctor"},
        {"role": "assistant", "content": "I've added 'Call the doctor' to your task list!"}
    ]
)

print(response2.content)  # "Great job! I've marked 'Call the doctor' as complete."
```

## Development

1. **Run Tests**:
   ```bash
   # Unit tests for intent recognition
   pytest tests/unit/test_intent_recognition.py

   # Integration tests with Gemini API
   pytest tests/integration/test_gemini_agent_integration.py

   # End-to-end conversation tests
   pytest tests/e2e/test_conversation_flow.py
   ```

2. **Local Testing**:
   ```bash
   # Start the agent service locally
   python -m backend.src.agents.agent_service
   ```

## Architecture Notes

- The agent is stateless - all conversation history is passed on each invocation
- MCP tools are registered with the agent as function definitions
- Tool calls are executed synchronously during message processing
- Responses include both natural language text and tool call records
- Error handling provides user-friendly messages while maintaining security