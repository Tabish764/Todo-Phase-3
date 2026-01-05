# Implementation Tasks: Fix AI Chatbot Integration Issues

## Phase 1: Setup & Project Initialization
- [x] T001 Set up backend project structure according to plan in backend/src/
  - AC: Directories exist: api/, services/, models/, database/, mcp/, utils/
- [x] T002 Set up frontend project structure according to plan in frontend/src/
  - AC: Directories exist: app/, components/, services/, hooks/, types/, lib/
- [x] T003 [P] Install required dependencies in backend (FastAPI, SQLModel, etc.)
  - AC: requirements.txt includes: fastapi, sqlmodel, asyncpg, python-dotenv, openai
- [x] T004 [P] Install required dependencies in frontend (@ai-sdk/react, etc.)
  - AC: package.json includes: @ai-sdk/react, ai, better-auth, next, react
- [x] T005 [P] Create backend/.env.example and document all required variables
  - AC: File contains: DATABASE_URL, OPENAI_API_KEY, BETTER_AUTH_SECRET, BETTER_AUTH_URL, CORS_ORIGINS
- [x] T006 [P] Validate environment variables loaded in config.py
  - AC: Settings class reads from os.getenv(), all vars accessible
- [x] T007 Set up database connection and models per data-model.md
  - AC: Database connection works, tables created on startup
- [x] T008 [P] Configure authentication with Better Auth
  - AC: Better Auth session available in frontend, user.id accessible in endpoints

## Phase 2: Foundational Components (Blocking Prerequisites)
- [x] T010 [P] Register chat router in backend main.py with /api prefix
  - AC: POST /api/{user_id}/chat endpoint responds 200, not 404
  - AC: Chat router imported and included before other routers
- [x] T011 [P] Create ToolExecutionService in backend/src/services/tool_execution_service.py
  - AC: Class with execute_tool(tool_name, args) → dict method
  - AC: Returns {\"status\": \"success\", \"result\": {...}} or {\"status\": \"error\", \"error\": \"...\"}
- [x] T012 [P] Create database models for Conversation, Message, Task per data-model.md
  - AC: Conversation(id, user_id, title, created_at, updated_at)
  - AC: Message(id, conversation_id, user_id, role, content, tool_calls, created_at)
  - AC: Task(id, user_id, title, description, completed, created_at, updated_at)
  - AC: Relationships defined (Conversation → Messages)
- [x] T013 [P] Implement API contract validation per contracts/chat-api-contract.md
  - AC: ChatRequest validates: conversation_id (optional int), message (required str, <10000 chars)
  - AC: ChatResponse returns: conversation_id (int), response (str), tool_calls (list)
  - AC: ToolCall contains: tool_name (str), arguments (dict), result (dict)
- [x] T014 [P] Set up frontend API service layer in frontend/src/services/chatService.ts
  - AC: sendMessage(userId: str, request: ChatRequest) → ChatResponse
  - AC: getConversations(userId: str) → Conversation[]
  - AC: getConversationHistory(userId: str, conversationId: int) → Message[]
  - AC: Proper error handling for 4xx and 5xx responses
- [x] T015 [P] Create TypeScript types for Message, Conversation, Task
  - AC: Types in frontend/src/types/chat.ts
  - AC: Message, ChatRequest, ChatResponse, ToolCall, Conversation interfaces

## Phase 2a: API Route Alignment (CRITICAL)
- [x] T016 [P] Audit all backend API routes for consistency
  - AC: All routes use /api prefix (not mixed with /api/v1)
  - AC: All routes follow {resource}/{id}/{sub-resource} pattern
  - AC: Document: Chat routes at /api/..., Conversation routes at /api/...
- [x] T017 [P] Update frontend service layer to call correct backend routes
  - AC: chatService methods match actual backend endpoints
  - AC: No 404 errors when calling conversations, messages, chat endpoints
- [x] T018 [P] Verify API contract alignment between frontend and backend
  - AC: Request/response schemas match between chatService.ts and chat_router.py
  - AC: All required fields present in responses

## Phase 3: ChatKit & Frontend Setup (P1 Dependency)
- [x] T070 [P] Replace custom chat components with @ai-sdk/react useChat hook
  - AC: useChat imported from @ai-sdk/react (not custom implementation)
  - AC: Messages, input, handleSubmit, isLoading from @ai-sdk/react
- [x] T071 [P] Create Next.js API route for chat proxy at frontend/src/app/api/chat/route.ts
  - AC: Accepts POST requests from frontend useChat hook
  - AC: Proxies to backend POST /api/{user_id}/chat
  - AC: Includes user_id and conversation_id in body
  - AC: Returns ChatResponse format
- [x] T072 [P] Update ChatKitWrapper to use official @ai-sdk/react components
  - AC: Maintains all existing functionality (message display, tool calls, errors, mobile)
  - AC: Uses official ChatKit components/styling
- [x] T073 [P] Verify ChatKit integration works end-to-end
  - AC: User can type message, send, see response
  - AC: Loading indicator shows during processing
  - AC: Tool calls display correctly

## Phase 4: [US1] Access Chat Interface (P1)
- [x] T020 [P] Add \"Chat\" navigation button to homepage in frontend/src/app/page.tsx
  - AC: Button visible on authenticated home page
  - AC: Button labeled \"💬 AI Chat Assistant\" or similar
  - AC: Clicking navigates to /chat
- [x] T021 [P] Create chat page route at frontend/src/app/chat/page.tsx
  - AC: Page is client component
  - AC: Page loads only for authenticated users
  - AC: Redirects to /login if not authenticated
- [x] T022 [P] Create conversation sidebar component in frontend/src/components/Chat/ConversationSidebar.tsx
  - AC: Displays list of user's conversations
  - AC: Shows conversation title and last updated date
  - AC: \"New Chat\" button visible
  - AC: Mobile responsive with collapsible drawer
- [x] T024 [P] Add authentication check to chat page
  - AC: useAuth() hook provides user.id
  - AC: Unauthenticated access redirected to /login
  - AC: Error boundary catches component errors
- [x] T025 [P] Implement navigation between dashboard and chat
  - AC: Sidebar link from chat to home
  - AC: Home link from chat to dashboard
  - AC: URL state preserved (conversation_id in query params)

## Phase 5: [US2] Send Message and Receive AI Response (P1)
- [x] T030 [P] Implement chat endpoint POST /api/{user_id}/chat in backend/src/api/v1/chat_router.py
  - AC: Accepts ChatRequest: {conversation_id?: int, message: str}
  - AC: If no conversation_id, creates new Conversation
  - AC: Stores user message in database
  - AC: Calls AI agent service to generate response
  - AC: Stores assistant response in database
  - AC: Returns ChatResponse: {conversation_id, response, tool_calls}
- [x] T031 [P] Set up @ai-sdk/react useChat hook in chat page
  - AC: useChat({ api: '/api/chat', body: { user_id, conversation_id } })
  - AC: Messages state auto-manages with @ai-sdk/react
- [x] T032 [P] Create API proxy handler in frontend/src/app/api/chat/route.ts
  - AC: Receives user message from @ai-sdk/react
  - AC: Calls backend /api/{user_id}/chat endpoint
  - AC: Returns response in expected format
- [x] T033 [P] [US2] Implement message display in chat interface
  - AC: User messages displayed in blue/right-aligned
  - AC: Assistant messages displayed in gray/left-aligned
  - AC: Messages render in chronological order
  - AC: Auto-scroll to latest message
- [x] T034 [P] [US2] Add loading indicators during AI processing
  - AC: \"Thinking...\" or skeleton appears while waiting
  - AC: Send button disabled during processing
  - AC: Input field disabled during processing
- [x] T035 [P] [US2] Handle conversation_id management
  - AC: New conversation: no conversation_id in request
  - AC: Existing conversation: conversation_id in request
  - AC: Backend returns conversation_id for new conversations
  - AC: Frontend tracks conversation_id in state
  - AC: URL includes conversation_id for refresh support

## Phase 6: [US3] Verify Tool Execution (P1)
- [x] T040 [P] [US3] Implement add_task tool in backend/src/services/tool_execution_service.py
  - AC: Input: {user_id, title, description?}
  - AC: Action: INSERT into tasks table
  - AC: Output: {\"status\": \"created\", \"task_id\": int, \"title\": str, \"created_at\": timestamp}
  - AC: Database verified: Task exists with completed=false
- [x] T041 [P] [US3] Implement list_tasks tool in backend/src/services/tool_execution_service.py
  - AC: Input: {user_id, status: \"all\"|\"pending\"|\"completed\"}
  - AC: Action: SELECT tasks filtered by user_id and optional status
  - AC: Output: {\"status\": \"success\", \"tasks\": [...], \"count\": int}
  - AC: Only returns user's own tasks (security check)
- [x] T042 [P] [US3] Implement complete_task tool in backend/src/services/tool_execution_service.py
  - AC: Input: {user_id, task_id}
  - AC: Action: UPDATE task SET completed=true
  - AC: Output: {\"status\": \"completed\", \"task_id\": int, \"title\": str}
  - AC: Database verified: Task.completed=true
- [x] T043 [P] [US3] Implement delete_task tool in backend/src/services/tool_execution_service.py
  - AC: Input: {user_id, task_id}
  - AC: Action: DELETE from tasks
  - AC: Output: {\"status\": \"deleted\", \"task_id\": int}
  - AC: Database verified: Task no longer exists
- [x] T044 [P] [US3] Implement update_task tool in backend/src/services/tool_execution_service.py
  - AC: Input: {user_id, task_id, title?, description?}
  - AC: Action: UPDATE task SET title/description
  - AC: Output: {\"status\": \"updated\", \"task_id\": int, \"title\": str}
  - AC: Database verified: Task fields updated
- [x] T045 [P] [US3] Implement tool execution loop in chat router
  - AC: After AI response, check for tool_calls array
  - AC: For each tool: call tool_execution_service.execute_tool(name, args)
  - AC: Capture result from tool execution
  - AC: Store tool results in message.tool_calls in database
  - AC: Return tool_calls with real results (not empty {})
  - AC: Handle tool execution errors gracefully
- [x] T046 [P] [US3] Return tool execution results to frontend
  - AC: ChatResponse includes tool_calls: [{tool_name, arguments, result}]
  - AC: result field contains actual tool execution result
  - AC: Error results: {\"status\": \"error\", \"error\": \"message\"}
- [x] T047 [P] [US3] Display tool call results in chat interface
  - AC: Tool calls expandable/collapsible in messages
  - AC: Shows tool_name, arguments, and result
  - AC: Icons indicate success/failure of tool execution
  - AC: User sees: \"✓ Added task: Buy milk (ID: 5)\"

## Phase 7: [US4] Access Conversation History (P2)
- [x] T050 [P] [US4] Implement GET /api/{user_id}/conversations endpoint
  - AC: Returns list of user's conversations
  - AC: Sorted by most recent first (updated_at DESC)
  - AC: Each conversation includes: id, user_id, title, created_at, updated_at
  - AC: Only returns conversations for authenticated user
- [x] T051 [P] [US4] Implement GET /api/{user_id}/conversations/{conversation_id}/messages endpoint
  - AC: Returns all messages for a conversation
  - AC: Sorted by created_at ASC (oldest first)
  - AC: Each message includes: id, role, content, tool_calls, created_at
  - AC: Verifies conversation belongs to user (404 if not)
- [x] T052 [P] [US4] Load conversation list in sidebar component
  - AC: On chat page load, fetch conversations
  - AC: Display each conversation with title and date
  - AC: \"New Chat\" button to start fresh conversation
- [x] T053 [P] [US4] Load conversation history when selected
  - AC: Clicking conversation loads all messages
  - AC: Messages display in chronological order
  - AC: URL updated to /chat?conversation_id=123
- [x] T054 [P] [US4] Implement conversation switching functionality
  - AC: User can switch between conversations without reloading
  - AC: Sidebar highlights current conversation
  - AC: Previous conversation closes, new one opens
- [x] T055 [P] [US4] Persist conversation history across page refreshes
  - AC: User refreshes page mid-conversation
  - AC: Conversation ID in URL: /chat?conversation_id=123
  - AC: Page reload restores conversation from backend
  - AC: All messages reload and display

## Phase 8: [US4] Conversation Title Generation (P2)
- [x] T060 [P] [US4] Auto-generate conversation titles from first message in backend
  - AC: When creating conversation, extract first 50 chars of first message
  - AC: Title = first_message[:50] (or until newline)
  - AC: Store title in conversation.title in database
  - AC: Example: \"Add buy groceries\" → title = \"Add buy groceries\"
- [x] T061 [P] [US4] Display conversation titles in sidebar
  - AC: Show title in sidebar instead of \"None\" or empty string
  - AC: Update title when displayed
  - AC: Truncate long titles with ellipsis

## Phase 8: [US2] ChatKit Library Integration (P1)
- [x] T070 [P] Replace custom chat components with @ai-sdk/react useChat hook
- [x] T071 [P] Create Next.js API route for chat proxy in frontend/src/app/api/chat/route.ts
- [x] T072 [P] Update ChatKitWrapper to use official components
- [x] T073 [P] Maintain existing functionality with new ChatKit implementation

## Phase 9: Error Handling & User Feedback

**Backend Error Handling:**
- [x] T080 [P] Implement backend error handling for empty/invalid messages (400)
  - AC: Empty message: return 400 {\"error\": \"Message cannot be empty\"}
  - AC: Message > 10000 chars: return 400 {\"error\": \"Message too long\"}
  - AC: Invalid user_id: return 400 {\"error\": \"Invalid user_id\"}
- [x] T081 [P] Implement backend error handling for invalid conversation_id (400)
  - AC: Non-integer conversation_id: return 400
  - AC: Negative conversation_id: return 400
  - AC: Non-existent conversation_id: return 404 {\"error\": \"Conversation not found\"}
- [x] T082 [P] Implement backend error handling for tool execution failures
  - AC: Tool not found: return error message to user
  - AC: Tool execution timeout: return 504 \"Tool execution timed out\"
  - AC: Tool database error: log error, return user-friendly message
  - AC: Invalid tool arguments: return 400 with validation error
- [x] T083 [P] Implement backend error handling for OpenAI API failures
  - AC: OpenAI API timeout: return 504 with retry message
  - AC: OpenAI API error: return 503 \"AI service unavailable\"
  - AC: Invalid API key: return 500 (don't expose key issue to user)
- [x] T084 [P] Implement backend error handling for database errors (500)
  - AC: Log full error stack
  - AC: Return generic 500: {\"error\": \"Database error occurred\"}
  - AC: Don't expose SQL or internal details to user

**Frontend Error Handling:**
- [x] T085 [P] Implement frontend error handling for unauthorized access (401)
  - AC: Receive 401 response
  - AC: Redirect to /login with message: \"Session expired. Please log in again.\"
  - AC: Clear any local chat state
- [x] T086 [P] Implement frontend error handling for not found errors (404)
  - AC: Conversation not found: \"This conversation was deleted\"
  - AC: Endpoint not found: \"Feature not available\"
- [x] T087 [P] Implement frontend error handling for server errors (500)
  - AC: Show error message: \"Something went wrong. Please try again.\"
  - AC: Provide \"Retry\" button to resend last message
  - AC: Log error with user_id for debugging
- [x] T088 [P] Implement frontend error handling for network timeouts
  - AC: Timeout after 30 seconds: \"Request timed out\"
  - AC: No network: \"No internet connection\"
  - AC: Provide retry option
- [x] T089 [P] Display user-friendly error messages in chat interface
  - AC: Error appears in dedicated error panel (not as message)
  - AC: Clear language (no technical jargon)
  - AC: Action button: \"Retry\" or \"Go back\"
  - AC: Color coding: red for errors, yellow for warnings

## Phase 10: Testing & Quality Assurance

**Backend Unit Tests:**
- [x] T090 [P] Write unit tests for ToolExecutionService
  - AC: test_add_task_creates_task_in_database()
  - AC: test_list_tasks_returns_user_tasks_only()
  - AC: test_complete_task_updates_completed_flag()
  - AC: test_delete_task_removes_from_database()
  - AC: test_update_task_modifies_title_or_description()
  - AC: test_tool_execution_with_invalid_user_id_fails()
  - AC: test_tool_execution_with_invalid_task_id_fails()
  - AC: Coverage: >80% of ToolExecutionService
- [x] T091 [P] Write unit tests for chat router endpoints
  - AC: test_chat_endpoint_with_empty_message_returns_400()
  - AC: test_chat_endpoint_creates_new_conversation_if_no_id()
  - AC: test_chat_endpoint_loads_existing_conversation()
  - AC: test_chat_endpoint_returns_conversation_id_in_response()
  - AC: test_chat_endpoint_stores_user_message_in_database()
  - AC: test_chat_endpoint_stores_assistant_response_in_database()
  - AC: Coverage: >80% of chat_router.py

**Frontend Component Tests:**
- [x] T092 [P] Write unit tests for frontend chat components
  - AC: test_chatkit_wrapper_renders_messages()
  - AC: test_chatkit_wrapper_sends_message_on_enter()
  - AC: test_chatkit_wrapper_disables_input_while_loading()
  - AC: test_conversation_sidebar_displays_list()
  - AC: test_conversation_sidebar_clicking_loads_conversation()
  - AC: test_tool_call_display_expands_on_click()
  - AC: test_error_display_shows_appropriate_error_message()
  - AC: Coverage: >80% of Chat components

**Integration & E2E Tests:**
- [x] T093 [P] Write integration tests for chat flow
  - AC: test_full_chat_flow_send_message_and_receive_response()
  - AC: test_tool_execution_flow_from_ai_to_database()
  - AC: test_conversation_persistence_across_messages()
  - AC: test_conversation_loading_from_sidebar_selection()
- [x] T094 [P] Write end-to-end tests for user stories using Playwright
  - AC: test_US1_authenticated_user_accesses_chat_page()
    - Login → Dashboard → Click Chat → Chat page loads
  - AC: test_US2_user_sends_message_and_receives_response()
    - Type \"Hello\" → Send → Receive response → Message displayed
  - AC: test_US3_ai_executes_tool_and_modifies_database()
    - User: \"Add buy milk\" → AI identifies tool → Tool executes → Task created
  - AC: test_US4_user_loads_conversation_history()
    - Create conversation → Navigate away → Reload → History appears
- [x] T095 [P] Verify test coverage exceeds 70% for critical paths
  - AC: Run: npm test (frontend) and pytest (backend)
  - AC: Generate coverage report
  - AC: Coverage >70% for: chatService, useChat, ToolExecutionService, chat_router

## Phase 11: Logging, Monitoring & Observability
- [x] T100 [P] Add logging to backend chat endpoint
  - AC: Log every chat message: {user_id, conversation_id, message_length, timestamp}
  - AC: Log tool execution: {tool_name, user_id, status (success/failure), duration}
  - AC: Log errors: {error_type, user_id, full_traceback, timestamp}
- [x] T101 [P] Add logging to tool execution service
  - AC: Log each tool call: {tool_name, input_args, execution_time}
  - AC: Log tool failures: {tool_name, error_message, user_id}
- [x] T102 [P] Add frontend client-side logging
  - AC: Log chat page load: {user_id, timestamp}
  - AC: Log message sends: {message_length, timestamp}
  - AC: Log errors with context: {error_type, user_id, additional_context}

## Phase 12: Polish & Cross-Cutting Concerns
- [x] T103 [P] Optimize frontend performance for large conversation histories
  - AC: Virtual scrolling for messages (100+ messages)
  - AC: Lazy load conversation list (paginate if many)
  - AC: Memoize components to prevent re-renders
- [x] T104 [P] Ensure mobile responsiveness for chat interface
  - AC: Chat works on 320px width screens
  - AC: Sidebar collapses to hamburger on mobile
  - AC: Input field accessible with mobile keyboard
  - AC: Messages readable on small screens
- [x] T105 [P] Add loading skeletons for better UX
  - AC: Skeleton for message list while loading
  - AC: Skeleton for conversation sidebar while loading
  - AC: Smooth transition from skeleton to real content
- [x] T106 [P] Implement smooth animations for message transitions
  - AC: Messages fade/slide in as they appear
  - AC: Loading indicator animates
  - AC: Error message slides in from top
- [x] T107 [P] Add accessibility features to chat components
  - AC: ARIA labels on buttons and inputs
  - AC: Keyboard navigation (Tab, Enter)
  - AC: Screen reader support for message roles
  - AC: WCAG AA compliance
- [x] T108 [P] Optimize API response times and implement caching
  - AC: Conversation list cache (5 min TTL)
  - AC: Recent messages cached locally
  - AC: Backend response time <500ms for chat endpoint
- [x] T109 [P] Implement proper error boundaries in React components
  - AC: Error boundary wraps chat page
  - AC: Catches component errors gracefully
  - AC: Displays fallback UI with reload option
- [x] T110 [P] Final integration testing and bug fixes
  - AC: All critical path tasks completed
  - AC: All user stories verified working
  - AC: No console errors or warnings
  - AC: All tests passing
  - AC: Performance benchmarks met

## Dependency Graph
```
Phase 1 (T001-008): Setup ✓
    ↓
Phase 2 (T010-015): Foundational Components ✓
    ↓
Phase 2a (T016-018): API Route Alignment ✓ ← CRITICAL
    ↓
Phase 3 (T070-073): ChatKit Integration ✓ ← MOVE HERE (before operations)
    ↓
Phase 4 (T020-025): Chat Access (US1) ✓
    ↓
Phase 5 (T030-035): Send/Receive (US2) ✓
    ↓
Phase 6 (T040-047): Tool Execution (US3) ✓ ← BLOCKER
    ↓
Phase 7 (T050-055): Conversation History (US4) ✓
    ↓
Phase 8 (T060-061): Conversation Titles ✓
    ↓
Phase 9 (T080-089): Error Handling ✓ (parallel with above)
    ↓
Phase 10 (T090-095): Testing ✓ (can start earlier, complete last)
    ↓
Phase 11 (T100-102): Logging & Observability ✓
    ↓
Phase 12 (T103-110): Polish & Final Testing ✓
```

## Parallel Execution Examples
- **Phase 1**: T001, T002, T003, T004, T005, T006, T007, T008 all parallel
- **Phase 2**: T010, T011, T012, T013, T014, T015 all parallel
- **Phase 2a**: T016, T017, T018 all parallel
- **Phase 3**: T070, T071, T072, T073 all parallel (blocks UI implementation)
- **Phase 4**: T020, T021, T022, T023, T024, T025 all parallel
- **Phase 5**: T030, T031, T032, T033, T034, T035 all parallel (after Phase 3)
- **Phase 6**: T040, T041, T042, T043, T044 parallel; T045, T046, T047 sequential
- **Phase 7**: T050, T051, T052, T053, T054, T055 all parallel
- **Phase 8**: T060, T061 parallel
- **Phase 9**: T080, T081, T082, T083, T084, T085, T086, T087, T088, T089 all parallel
- **Phase 10**: T090, T091, T092, T093, T094, T095 can be parallel (but depend on earlier phases)
- **Phase 11**: T100, T101, T102 parallel
- **Phase 12**: T103, T104, T105, T106, T107, T108, T109, T110 parallel

## REVISED Critical Path (Must Complete In Order)
1. **T001-008** (Project Setup) - **BLOCKER** - 30 min
2. **T010** (Chat Router Registration) - **BLOCKER** - 5 min
3. **T011** (ToolExecutionService) - **BLOCKER** - 3-4 hours
4. **T012** (Database Models) - **BLOCKER** - 1-2 hours
5. **T016-018** (API Route Alignment) - **CRITICAL** - 30 min
6. **T070-073** (ChatKit Integration) - **BLOCKER FOR UI** - 2 hours
7. **T020-025** (Chat UI Access) - **BLOCKER FOR MESSAGES** - 1-2 hours
8. **T030-035** (Send/Receive Messages) - **BLOCKER FOR TOOLS** - 2-3 hours
9. **T040-047** (Tool Execution) - **CORE FEATURE** - 3-4 hours
10. **T090-095** (Testing) - **VALIDATION** - 4-5 hours

**Estimated Total**: 20-25 hours of focused development

## Implementation Strategy
- **MVP Scope**: Complete Phases 1-6 (T001-T047)
  - Users can: Chat with AI, AI executes tasks, tool results returned
  - Deliverable: Fully functional chatbot with task management
- **Phase 2 Scope**: Complete Phases 7-10 (T050-T095)
  - Users can: Access conversation history, see titles, full test coverage
- **Phase 3 Scope**: Complete Phases 11-12 (T100-T110)
  - Logging, performance optimization, accessibility, polish
- **Parallel Work**: Tests (T090-095) can start during Phase 6, complete before Phase 7
- **Risk Mitigation**: 
  - Complete critical path first
  - If blocked on any critical task, escalate immediately
  - Validate each phase before moving to next
  - Run tests after each phase

## Success Criteria (Everything Below = \"Done\")
- ✅ User logs in → sees Chat button
- ✅ Clicks Chat → navigates to /chat
- ✅ Chat interface loads with empty message list
- ✅ Types \"Add task: Buy milk\" → sends message
- ✅ AI identifies add_task tool → calls it
- ✅ add_task executes → task created in database
- ✅ Response: \"Added task: Buy milk (ID: 5)\"
- ✅ User sees tool call visualization
- ✅ Tool result shows in message
- ✅ User refreshes page → conversation persists
- ✅ Sidebar shows conversation list with titles
- ✅ User can click previous conversation → loads history
- ✅ All tests passing (>70% coverage)
- ✅ No console errors/warnings
- ✅ Mobile responsive
- ✅ Error handling works for all failure cases