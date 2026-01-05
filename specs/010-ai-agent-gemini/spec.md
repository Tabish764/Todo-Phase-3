# Feature Specification: Todo AI Chatbot - AI Agent Configuration (OpenAI Agents SDK with Gemini API)

**Feature Branch**: `010-ai-agent-gemini`
**Created**: 2025-12-27
**Status**: Draft
**Dependencies**:
- Feature 008: MCP Server Tools (all 5 tools must be available)
- Feature 009: Chat API Endpoint (provides message context to agent)

## Overview

Configure and implement an AI agent using **OpenAI Agents SDK** connected to **Google Gemini API** that understands natural language commands for task management, intelligently selects and invokes appropriate MCP tools, maintains conversational context, and generates helpful responses to users.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Creation (Priority: P1)

As a user, I want to tell the AI to add tasks using natural, everyday language so that I don't have to learn specific commands or syntax.

**Why this priority**: This is the fundamental value proposition of the AI chatbot - making task management feel like a natural conversation rather than a technical interface.

**Independent Test**: Can be tested by sending various phrasings for task creation (e.g., "add buy milk", "I need to remember to call mom", "create a task for the meeting") and verifying the AI correctly identifies the intent and calls add_task tool.

**Acceptance Scenarios**:

1. **Given** a user says "Add a task to buy groceries", **When** the AI agent processes the message, **Then** it calls add_task tool with title="Buy groceries"
2. **Given** a user says "I need to remember to call mom", **When** the AI agent processes the message, **Then** it calls add_task tool with title="Call mom"
3. **Given** a user says "Create a task: Review project proposal with detailed notes", **When** the AI agent processes the message, **Then** it calls add_task with title and description extracted appropriately
4. **Given** a user says "Don't let me forget about the dentist appointment", **When** the AI agent processes the message, **Then** it calls add_task with appropriate task title

---

### User Story 2 - Intelligent Task Listing with Filters (Priority: P1)

As a user, I want to ask about my tasks in natural language and have the AI understand what subset of tasks I'm interested in.

**Why this priority**: Users need to quickly access different views of their tasks (all, pending, completed) without remembering exact filter syntax.

**Independent Test**: Can be tested by asking questions like "show my tasks", "what's pending?", "what have I completed?" and verifying the correct list_tasks filter is applied.

**Acceptance Scenarios**:

1. **Given** a user asks "Show me all my tasks", **When** the AI agent processes the message, **Then** it calls list_tasks with status="all"
2. **Given** a user asks "What's pending?", **When** the AI agent processes the message, **Then** it calls list_tasks with status="pending"
3. **Given** a user asks "What have I completed?", **When** the AI agent processes the message, **Then** it calls list_tasks with status="completed"
4. **Given** a user asks "Show my todo list", **When** the AI agent processes the message, **Then** it calls list_tasks with appropriate filter

---

### User Story 3 - Task Completion and Deletion (Priority: P1)

As a user, I want to mark tasks as done or remove them using conversational language without needing to remember task IDs.

**Why this priority**: Core task management operations must work intuitively through natural language.

**Independent Test**: Can be tested by saying "mark task 3 as done" or "I finished the groceries task" and verifying the correct complete_task or delete_task tool is called.

**Acceptance Scenarios**:

1. **Given** a user says "Mark task 3 as complete", **When** the AI agent processes the message, **Then** it calls complete_task with task_id=3
2. **Given** a user says "Delete task 5", **When** the AI agent processes the message, **Then** it calls delete_task with task_id=5
3. **Given** a user says "I finished buying groceries", **When** the AI agent processes the message, **Then** it first calls list_tasks to find the matching task, then calls complete_task
4. **Given** a user says "Remove the meeting task", **When** the AI agent processes the message, **Then** it first identifies which task matches, then calls delete_task

---

### User Story 4 - Multi-Step Interactions for Ambiguous Requests (Priority: P2)

As a user, when my request is ambiguous or incomplete, I want the AI to ask clarifying questions rather than guessing incorrectly.

**Why this priority**: This prevents errors and frustration when users don't provide exact task IDs or when multiple tasks could match their description.

**Independent Test**: Can be tested by saying "delete the buy task" when multiple tasks contain "buy" and verifying the AI asks which specific task to delete.

**Acceptance Scenarios**:

1. **Given** a user says "Mark the groceries task as done" and multiple tasks contain "groceries", **When** the AI agent processes the message, **Then** it lists the matching tasks and asks which one to complete
2. **Given** a user provides a partial task description, **When** the AI cannot determine the exact task, **Then** it asks for clarification with specific options
3. **Given** a user's follow-up response clarifies their intent, **When** the AI processes the clarification, **Then** it executes the originally intended action

---

### User Story 5 - Helpful Confirmations and Error Handling (Priority: P2)

As a user, I want clear confirmations when actions succeed and helpful guidance when something goes wrong.

**Why this priority**: Good feedback makes the chatbot feel responsive and trustworthy, while poor feedback leaves users confused.

**Independent Test**: Can be tested by performing various actions and errors (successful task creation, attempting to delete non-existent task) and verifying response quality.

**Acceptance Scenarios**:

1. **Given** the AI successfully creates a task, **When** it responds to the user, **Then** it includes a friendly confirmation with the task title
2. **Given** the AI successfully completes a task, **When** it responds to the user, **Then** it acknowledges the completion with an encouraging message
3. **Given** an MCP tool returns an error (e.g., "Task not found"), **When** the AI processes the error, **Then** it explains what went wrong and suggests next steps
4. **Given** the user's intent is unclear, **When** the AI responds, **Then** it asks a specific clarifying question rather than making assumptions

---

### User Story 6 - Conversational Context Maintenance (Priority: P2)

As a user having an ongoing conversation, I want the AI to remember what we've discussed so I can refer back to previous topics naturally.

**Why this priority**: This enables natural, flowing conversations where users don't have to repeat information or re-explain context.

**Independent Test**: Can be tested by having a multi-turn conversation where later messages reference earlier topics and verifying the AI maintains appropriate context.

**Acceptance Scenarios**:

1. **Given** a user previously mentioned a task, **When** the user refers to "that task" later, **Then** the AI understands the reference from conversation history
2. **Given** a user asks a follow-up question, **When** the AI responds, **Then** it considers the context of previous messages in the conversation
3. **Given** a conversation has multiple topics, **When** the AI generates responses, **Then** it maintains awareness of the full conversation flow

---

### Edge Cases

- What happens when the user gives a command that doesn't map to any MCP tool?
- How does the agent handle messages that are pure greetings or small talk (e.g., "hello", "thanks")?
- What occurs when an MCP tool call fails but the conversation should continue?
- How does the agent respond to commands with typos or grammatical errors?
- What happens when the user asks about capabilities the agent doesn't have?
- How does the agent handle very long or complex multi-part requests?
- What occurs when the Gemini API is rate-limited or unavailable?
- How does the agent respond to commands in languages other than English?

---

## Requirements *(mandatory)*

### Functional Requirements

#### OpenAI Agents SDK Configuration

- **FR-001**: System MUST use OpenAI Agents SDK for agent orchestration and tool calling
- **FR-002**: System MUST configure the SDK to route requests to Google Gemini API instead of OpenAI API
- **FR-003**: Agent MUST be initialized with clear system instructions defining its role and capabilities
- **FR-004**: Agent MUST have access to all 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **FR-005**: Agent MUST receive the complete message array including conversation history on each invocation
- **FR-006**: Agent MUST support streaming responses for better user experience (optional but recommended)

#### Agent Personality and Behavior

- **FR-007**: Agent MUST present itself as a helpful task management assistant
- **FR-008**: Agent MUST use a friendly, conversational, and encouraging tone
- **FR-009**: Agent MUST avoid technical jargon and speak in natural language
- **FR-010**: Agent MUST NOT use emojis unless the user uses them first
- **FR-011**: Agent MUST be concise in responses while being complete
- **FR-012**: Agent MUST proactively offer help when users seem unsure
- **FR-013**: Agent MUST celebrate user accomplishments (e.g., completing tasks)

#### Natural Language Understanding

- **FR-014**: Agent MUST recognize task creation intent from phrases like:
  - "add [task]"
  - "create [task]"
  - "remember [task]"
  - "I need to [task]"
  - "don't forget [task]"
  - "remind me to [task]"

- **FR-015**: Agent MUST recognize task listing intent from phrases like:
  - "show tasks"
  - "list tasks"
  - "what's pending"
  - "what have I done"
  - "see my todos"
  - "what do I need to do"

- **FR-016**: Agent MUST recognize task completion intent from phrases like:
  - "mark [task] as done"
  - "complete [task]"
  - "I finished [task]"
  - "done with [task]"
  - "[task] is complete"

- **FR-017**: Agent MUST recognize task deletion intent from phrases like:
  - "delete [task]"
  - "remove [task]"
  - "cancel [task]"
  - "get rid of [task]"

- **FR-018**: Agent MUST recognize task update intent from phrases like:
  - "change [task]"
  - "update [task]"
  - "rename [task]"
  - "modify [task]"
  - "edit [task]"

#### Tool Selection Logic

- **FR-019**: Agent MUST call add_task when user expresses intent to create a new task
- **FR-020**: Agent MUST call list_tasks when user wants to view their tasks
- **FR-021**: Agent MUST call complete_task when user indicates a task is finished
- **FR-022**: Agent MUST call delete_task when user wants to remove a task
- **FR-023**: Agent MUST call update_task when user wants to modify an existing task
- **FR-024**: Agent MUST extract user_id from conversation context and pass it to all MCP tools
- **FR-025**: Agent MUST extract task_id when explicitly mentioned by user
- **FR-026**: When task_id is not provided but needed, agent MUST first call list_tasks to help identify the task
- **FR-027**: Agent MAY chain multiple tool calls in a single response when appropriate

#### Response Generation

- **FR-028**: Agent MUST confirm successful actions with natural language (e.g., "I've added 'Buy groceries' to your list!")
- **FR-029**: Agent MUST format task lists in a clear, readable manner
- **FR-030**: Agent MUST include task details (title, ID) when listing tasks
- **FR-031**: Agent MUST explain errors in user-friendly terms without exposing technical details
- **FR-032**: Agent MUST provide actionable next steps when errors occur
- **FR-033**: Agent MUST ask clarifying questions when user intent is ambiguous
- **FR-034**: Agent MUST not repeat the same information unnecessarily

#### Error Handling

- **FR-035**: When MCP tool returns "Task not found", agent MUST explain the task doesn't exist and offer to list available tasks
- **FR-036**: When MCP tool returns "Unauthorized", agent MUST explain the user doesn't have access to that task
- **FR-037**: When user request is unclear, agent MUST ask for clarification rather than guessing
- **FR-038**: When Gemini API fails, agent MUST gracefully handle the error and inform the user
- **FR-039**: When multiple tasks match a description, agent MUST list them and ask user to specify
- **FR-040**: Agent MUST log all errors for debugging purposes

#### Context Management

- **FR-041**: Agent MUST receive full conversation history on every invocation
- **FR-042**: Agent MUST consider previous messages when interpreting current message
- **FR-043**: Agent MUST maintain awareness of tasks discussed earlier in the conversation
- **FR-044**: Agent MUST use conversation history to resolve ambiguous references (e.g., "that task", "the groceries one")

### Key Entities *(include if feature involves data)*

- **AgentConfiguration**: Settings for OpenAI Agents SDK including model selection, temperature, system instructions, and Gemini API endpoint
- **SystemInstructions**: The base prompt that defines agent personality, capabilities, and behavior guidelines
- **ToolDefinition**: JSON schema definitions for each MCP tool that the agent can invoke
- **MessageContext**: The array of messages (system, user, assistant) that provides conversation history to the agent
- **ToolCall**: A record of the agent invoking an MCP tool with specific arguments
- **AgentResponse**: The agent's generated text response plus any tool calls made

---

## Technical Specifications

### OpenAI Agents SDK with Gemini API Integration

**Agent Initialization:**
- Use OpenAI Agents SDK Runner
- Configure base_url to point to Gemini API endpoint
- Provide Gemini API key for authentication
- Set model to appropriate Gemini model (e.g., gemini-pro)
- Configure temperature and other generation parameters

**System Instructions Template:**

```
You are a helpful task management assistant. Your purpose is to help users manage their todo list through natural conversation.

Your capabilities:
- Create new tasks when users mention things they need to do
- List tasks with filtering (all, pending, completed)
- Mark tasks as complete when users finish them
- Delete tasks when users want to remove them
- Update tasks when users want to modify them

Guidelines:
- Be friendly, conversational, and encouraging
- Confirm all actions clearly
- When you don't understand, ask for clarification
- When errors occur, explain them in simple terms
- When users accomplish tasks, celebrate with them
- Keep responses concise but complete
- Never assume - if ambiguous, ask

The user you're talking to is: {user_id}
Always pass this user_id to all tool calls.
```

**Tool Configuration:**
Each MCP tool must be registered with the agent including:
- Tool name
- Description
- Input parameters (JSON schema)
- Required vs optional parameters

### Message Flow

**Step 1: Receive Context from Chat Endpoint**
- Chat endpoint passes message array to agent
- Array includes: system instructions, conversation history, current message
- Agent is stateless - receives full context every time

**Step 2: Process with Gemini API**
- OpenAI Agents SDK sends context to Gemini API
- Gemini processes message and decides if tools are needed
- Gemini may invoke zero, one, or multiple tools

**Step 3: Execute Tool Calls**
- When Gemini decides to call a tool, SDK invokes the corresponding MCP tool
- MCP tool executes (e.g., add_task creates database record)
- Tool returns result to SDK
- SDK passes result back to Gemini

**Step 4: Generate Response**
- Gemini generates natural language response incorporating tool results
- Response is contextual and conversational
- Response includes confirmations of actions taken

**Step 5: Return to Chat Endpoint**
- SDK returns agent response text and tool call records
- Chat endpoint stores response and returns to frontend

### Natural Language Processing Patterns

**Intent Recognition:**
The agent should recognize these intent patterns:

| User Input | Recognized Intent | Tool Call | Parameters Extracted |
|------------|------------------|-----------|---------------------|
| "Add buy milk" | Create task | add_task | title="Buy milk" |
| "I need to call the dentist" | Create task | add_task | title="Call the dentist" |
| "Show my tasks" | List tasks | list_tasks | status="all" |
| "What's pending?" | List tasks | list_tasks | status="pending" |
| "Task 5 is done" | Complete task | complete_task | task_id=5 |
| "Delete task 3" | Delete task | delete_task | task_id=3 |
| "Change task 1 to 'Call mom tonight'" | Update task | update_task | task_id=1, title="Call mom tonight" |

**Multi-Turn Handling:**
When task ID is not provided:
1. Agent calls list_tasks to show relevant tasks
2. Agent asks user to specify which task
3. Agent waits for user's clarification
4. Agent executes intended action with correct task_id

**Example:**
- User: "Mark the groceries task as done"
- Agent: Calls list_tasks → finds tasks #3 "Buy groceries", #7 "Buy groceries and fruits"
- Agent: "I found two tasks related to groceries: #3 'Buy groceries' and #7 'Buy groceries and fruits'. Which one did you complete?"
- User: "The first one"
- Agent: Calls complete_task(task_id=3) → "Great job! I've marked 'Buy groceries' as complete."

### Response Templates

**Task Creation:**
- "I've added '{title}' to your task list!"
- "Got it! '{title}' is now on your todo list."
- "Task created: '{title}'"

**Task Listing (Empty):**
- "You don't have any tasks yet. Want to add one?"
- "Your task list is empty. What would you like to accomplish?"

**Task Listing (With Results):**
- "Here are your {status} tasks: {task_list}"
- "You have {count} {status} tasks: {task_list}"

**Task Completion:**
- "Nice work! I've marked '{title}' as complete."
- "Awesome! '{title}' is done. Keep up the great work!"
- "Great job completing '{title}'!"

**Task Deletion:**
- "I've removed '{title}' from your list."
- "'{title}' has been deleted."

**Task Update:**
- "I've updated '{old_title}' to '{new_title}'."
- "Task updated successfully!"

**Errors:**
- "I couldn't find that task. Would you like to see all your tasks?"
- "That task doesn't exist. Use 'show tasks' to see your current list."
- "Something went wrong: {error_explanation}. {suggestion}"

**Ambiguity:**
- "I found {count} tasks matching '{description}': {task_list}. Which one did you mean?"
- "Could you clarify which task you're referring to?"

**Small Talk:**
- "Hello! I'm here to help you manage your tasks. What would you like to do?"
- "You're welcome! Anything else I can help you with?"

### Configuration Parameters

**Model Settings:**
- Model: gemini-pro (or latest stable Gemini model)
- Temperature: 0.7 (balance between creativity and consistency)
- Max tokens: 1000 (sufficient for responses)
- Top-p: 0.9
- Top-k: 40

**Tool Calling:**
- Allow multiple tool calls per response: Yes
- Tool choice: Auto (let model decide when to use tools)
- Parallel tool calls: Yes (when independent)

**Rate Limiting:**
- Implement retry logic for rate limit errors
- Exponential backoff: Start at 1s, max 32s
- Max retries: 3

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Agent correctly identifies task creation intent in 95%+ of test cases
- **SC-002**: Agent correctly identifies task listing intent in 95%+ of test cases
- **SC-003**: Agent correctly identifies completion/deletion intent in 95%+ of test cases
- **SC-004**: Agent successfully extracts task titles from natural language in 90%+ of cases
- **SC-005**: Agent makes appropriate tool calls (correct tool, correct parameters) in 90%+ of cases
- **SC-006**: Agent generates user-friendly, non-technical responses in 100% of interactions
- **SC-007**: Agent asks for clarification when faced with ambiguity in 100% of cases
- **SC-008**: Agent successfully handles MCP tool errors and provides helpful guidance in 100% of error cases
- **SC-009**: Agent maintains conversation context across multiple turns in 95%+ of cases
- **SC-010**: Agent responds within 5 seconds for single-tool interactions
- **SC-011**: Agent responds within 8 seconds for multi-tool interactions

### Quality Metrics

- **QM-001**: User satisfaction with agent responses (subjective, aim for "helpful" feedback)
- **QM-002**: Number of clarification questions needed per user request (lower is better, target <20%)
- **QM-003**: Accuracy of tool parameter extraction (target >90%)
- **QM-004**: Natural language quality of responses (no technical jargon, friendly tone)
- **QM-005**: Context retention across conversation turns (measured by successful pronoun resolution)

### Testing Requirements

- **TR-001**: Unit tests for intent recognition patterns (all intent types covered)
- **TR-002**: Unit tests for tool selection logic (correct tool chosen for each intent)
- **TR-003**: Integration tests with actual Gemini API calls
- **TR-004**: Integration tests with MCP tool invocations
- **TR-005**: Multi-turn conversation tests (3+ turn exchanges)
- **TR-006**: Ambiguity handling tests (multiple matching tasks)
- **TR-007**: Error handling tests (tool failures, API failures)
- **TR-008**: Edge case tests (typos, unclear commands, small talk)
- **TR-009**: Performance tests (response time under load)
- **TR-010**: Context maintenance tests (references to previous messages)