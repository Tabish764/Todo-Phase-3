# Data Model: Todo AI Chatbot - AI Agent Configuration (OpenAI Agents SDK with Gemini API)

## Entity: AgentConfiguration
- **Fields**:
  - model_name: String (e.g., "gemini-pro", "gemini-1.5-pro")
  - temperature: Float (default: 0.7, range: 0.0-1.0)
  - max_tokens: Integer (default: 1000)
  - top_p: Float (default: 0.9)
  - top_k: Integer (default: 40)
  - api_key: String (stored securely, not in plain text)
  - system_instructions: String (the base prompt defining agent behavior)

- **Validation Rules**:
  - model_name must be a valid Gemini model
  - temperature must be between 0.0 and 1.0
  - max_tokens must be positive
  - top_p must be between 0.0 and 1.0
  - top_k must be positive

- **Relationships**:
  - N/A (configuration is used by the agent service)

## Entity: ToolDefinition
- **Fields** (as part of tool definitions):
  - name: String (e.g., "add_task", "list_tasks", "complete_task", "delete_task", "update_task")
  - description: String (purpose of the tool)
  - parameters: Dict (JSON schema for tool parameters)
  - required_parameters: List[String] (required parameter names)

- **Validation Rules**:
  - name must match one of the supported MCP tool names
  - parameters must follow JSON Schema specification
  - required_parameters must be a subset of parameters

- **Relationships**:
  - Used by the agent to determine when to call MCP tools

## Entity: MessageContext
- **Fields** (as part of the message array passed to the agent):
  - role: String (Enum: 'system', 'user', 'assistant')
  - content: String (the message content)
  - timestamp: DateTime (when the message was created)

- **Validation Rules**:
  - role must be one of the allowed values
  - content must not be empty
  - timestamp must be in the past or present

- **Relationships**:
  - Forms the conversation history for the agent

## Entity: ToolCall
- **Fields** (embedded in agent responses):
  - tool_name: String (name of the MCP tool called)
  - arguments: Object (arguments passed to the tool)
  - result: Object (result returned by the tool)

- **Validation Rules**:
  - tool_name must match one of the registered MCP tools
  - arguments must match the expected schema for the tool
  - result must be a valid response from the tool

- **Relationships**:
  - Part of AgentResponse entity

## Entity: AgentResponse
- **Fields**:
  - content: String (the agent's natural language response)
  - tool_calls: List[ToolCall] (optional, list of tools invoked by the agent)
  - timestamp: DateTime (when the response was generated)

- **Validation Rules**:
  - content must not be empty
  - tool_calls must be valid if present
  - timestamp must be in the past or present

- **Relationships**:
  - Returned to the chat endpoint to be sent to the user

## State Transitions
- AgentConfiguration: Created during agent initialization, updated during configuration changes
- MessageContext: Added for each user message and assistant response
- ToolCall: Created when agent decides to invoke an MCP tool
- AgentResponse: Generated for each user request

## Indexes
- N/A (these are primarily in-memory objects used for API requests)