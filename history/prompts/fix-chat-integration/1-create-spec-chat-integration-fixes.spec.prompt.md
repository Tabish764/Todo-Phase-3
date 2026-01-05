---
id: 1
title: Create Spec for Chat Integration Fixes
stage: spec
date: 2025-12-30
model: Claude Sonnet 4.5
feature: fix-chat-integration
branch: 001-fix-chat-integration
user: Claude user
command: /sp.specify EXECUTIVE OVERVIEW
labels: [spec, ai-chatbot, integration, fixes]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-fix-chat-integration/spec.md
  - specs/001-fix-chat-integration/checklists/requirements.md
tests: []
---

# Create Spec for Chat Integration Fixes

## PROMPT_TEXT

EXECUTIVE OVERVIEW
Phase 3 has structural components but critical integration gaps prevent end-to-end functionality. This spec addresses all blocking issues:

Chat endpoint unreachable (not registered)
MCP tools not executed (no task modifications)
Chatbot invisible to users (no navigation)
Custom components instead of ChatKit library
Zero test coverage
API route misalignment
Target: Deliver fully functional, spec-compliant AI chatbot with working tool execution.

ISSUE #1: CHAT ENDPOINT NOT REGISTERED (CRITICAL)
Problem
chat_router.py exists but is never included in main.py
Frontend calls POST /api/{user_id}/chat but endpoint returns 404
Entire chat system is broken at the HTTP level
Root Cause
Solution Specification
Requirement 1.1: Register Chat Router in Main App

What to do:

Import chat_router from src.api.v1.chat_router
Include it in FastAPI app BEFORE other routers
Use prefix /api to match frontend expectations
Acceptance Criteria:

✅ POST /api/{user_id}/chat endpoint responds 200 OK (not 404)
✅ Accepts ChatRequest with conversation_id (optional) and message (required)
✅ Returns ChatResponse with conversation_id, response, tool_calls
✅ Can test with: curl -X POST http://localhost:8000/api/testuser/chat -H "Content-Type: application/json" -d '{"message":"hello"}'
Code Location:

File: main.py
Lines: ~84-87 (where other routers included)
Action: Add import + include_router call
Expected Result After Fix:

ISSUE #2: MCP TOOLS NOT EXECUTED (CRITICAL)
Problem
AI Agent identifies which tool to use (e.g., "add_task")
Tool is mentioned but never executed
No database updates occur
Tool results hardcoded as empty: "result": {}
User says "Add buy milk" → AI says it will → nothing actually added to database
Root Cause
In chat_router.py, lines 155-180:

Solution Specification
Requirement 2.1: Implement Tool Execution Loop

Architecture:

What to do:

Create Tool Execution Service

New file: backend/src/services/tool_execution_service.py
Purpose: Execute MCP tools by name
Methods:
execute_tool(tool_name: str, arguments: dict) → dict
Looks up tool in registry
Calls tool's async execute method
Returns result dict
Modify Chat Router to Execute Tools

File: chat_router.py
After AI returns tool_calls (line ~155):
For each tool_call:
Execute the tool
Capture result
Store in database with message
Tool Execution Flow

Acceptance Criteria:

✅ User sends: "Add task: Buy groceries"
✅ AI identifies: add_task tool needed
✅ Backend EXECUTES add_task with title="Buy groceries", user_id=user's_id
✅ Database UPDATES: New task created with id, title, completed=false
✅ Result returned: {"task_id": 5, "status": "created", "title": "Buy groceries"}
✅ User sees in chat: "Added task: Buy groceries (ID: 5)"
✅ Can verify: Task appears in /api/{user_id}/tasks list
Tool Specification (Each Tool):

Tool: add_task

Input: {"user_id": "...", "title": "...", "description": "..."}
Action: INSERT into tasks table
Output: {"task_id": <int>, "status": "created", "title": "...", "created_at": "..."}
Database: INSERT with user_id, title, description, completed=false, created_at=now, updated_at=now
Tool: list_tasks

Input: {"user_id": "...", "status": "all|pending|completed"}
Action: SELECT from tasks filtered by status
Output: {"tasks": [{"id": 1, "title": "...", "completed": false, ...}], "count": 5}
Database: SELECT WHERE user_id=? AND (completed=? if status filtered)
Tool: complete_task

Input: {"user_id": "...", "task_id": 1}
Action: UPDATE task SET completed=true
Output: {"task_id": 1, "status": "completed", "title": "...", "updated_at": "..."}
Database: UPDATE WHERE id=? AND user_id=? SET completed=true, updated_at=now
Tool: delete_task

Input: {"user_id": "...", "task_id": 1}
Action: DELETE from tasks
Output: {"task_id": 1, "status": "deleted", "title": "..."}
Database: DELETE WHERE id=? AND user_id=?
Tool: update_task

Input: {"user_id": "...", "task_id": 1, "title": "...", "description": "..."}
Action: UPDATE task SET title/description
Output: {"task_id": 1, "status": "updated", "title": "...", "updated_at": "..."}
Database: UPDATE WHERE id=? AND user_id=? SET title/description, updated_at=now
ISSUE #3: NO NAVIGATION TO CHATBOT (CRITICAL)
Problem
/chat route exists and works (if you manually navigate)
But zero navigation links from main app
User has no way to discover or access chatbot
Dashboard only shows Task Manager
Root Cause
In page.tsx:

No button/link to chat
Entire page is task-focused
User never sees chat as an option
Solution Specification
Requirement 3.1: Add Chat Navigation to Dashboard

What to do:

Add a navigation button/link on home page pointing to /chat
Make it prominent (same level as task section)
Show it only when authenticated
Location to Add Button:

File: page.tsx
Find: Header section (lines ~120-140)
Where: Next to user email and logout button, OR in a new "Navigation" section
Button Specification:

Acceptance Criteria:

✅ Authenticated user sees button/link on home page
✅ Clicking button navigates to /chat
✅ Chat page loads with sidebar and empty messages
✅ User can type message and get response
✅ Message appears in chat history
Alternative Approach (Better UX):
Add navigation tabs/menu:

At top of page, showing current section. Allows switching between Task Manager and Chat without homepage.

ISSUE #4: NOT USING OPENAI CHATKIT (CRITICAL)
Problem
Spec requires: "Use OpenAI ChatKit component library"
Current implementation: Custom HTML/Tailwind components
@ai-sdk/react package installed but never used
Violates spec requirement
Root Cause
ChatKitWrapper.tsx is a manual implementation with:

Not using @ai-sdk/react or official ChatKit.

Solution Specification
Requirement 4.1: Integrate @ai-sdk-react useChat Hook

What to do:

Replace custom useChat hook with @ai-sdk-react built-in
Use ChatKit components if available
Keep existing integration with backend
Option A: Use @ai-sdk-react (Recommended)

Option B: If ChatKit component exists

What Needs to Happen:

Create Next.js API Route (if using Option A):

File: frontend/src/app/api/chat/route.ts
Purpose: Proxy requests to backend
Takes frontend message → calls POST /api/{user_id}/chat → returns response
Update ChatKitWrapper:

Use @ai-sdk-react's useChat hook
Keep message display logic
Keep error handling
Keep tool call visualization
Keep Conversation Sidebar:

Still manages conversation list
Still loads history on select
Works with new useChat hook
Acceptance Criteria:

✅ Using @ai-sdk-react provided hooks
✅ Official ChatKit components if available
✅ All existing features work (history, tool calls, errors, mobile)
✅ Message display same as before
✅ No breaking changes to conversation loading
Fallback (If ChatKit not available):

Keep custom components but follow @ai-sdk-react pattern
Import and use official useChat hook
Maintain spec compliance with custom UI layer on top
ISSUE #5: ZERO TEST COVERAGE (CRITICAL - CONSTITUTIONAL VIOLATION)
Problem
Spec requires: "Test-First / TDD (Non-Negotiable)"
Project has: Zero tests
integration folder is empty
Violates constitutional requirement
Root Cause
Tests were never written during implementation.

Solution Specification
Requirement 5.1: Implement Test Suite

Test Structure:

Unit Tests (Components)

ChatKitWrapper.test.tsx

Test: Component renders with empty messages
Test: Send button disabled when input empty
Test: Input value updates on change
Test: Submit sends message via onSendMessage prop
Test: Loading indicator shows when isLoading=true
Test: Error message displays when error prop set
ConversationSidebar.test.tsx

Test: Renders conversation list
Test: "New Chat" button calls onNewConversation
Test: Click conversation calls onSelectConversation with id
Test: Current conversation highlighted
ToolCallDisplay.test.tsx

Test: Renders tool name
Test: Expand/collapse toggles details
Test: Shows arguments JSON
Test: Shows result JSON
ErrorDisplay.test.tsx

Test: Renders error message
Test: Detects error types (auth, network, timeout)
Test: Shows appropriate error icon/message
Integration Tests (Hooks)

useChat.test.ts
Test: sendMessage calls chatService
Test: loadConversation fetches history
Test: startNewConversation clears state
Test: Timeout detection after 30 seconds
Test: Error state updates on failure
End-to-End Tests (Chat Flow)

chat.e2e.spec.ts (using Playwright)
Test: Login → navigate to chat → see empty interface
Test: Type message → send → see user message
Test: Wait for response → see assistant message
Test: Click conversation in sidebar → load history
Test: Refresh page → conversation persists
Test Configuration:

Framework: Jest for unit/integration
E2E: Playwright
Coverage target: 80%+ for critical paths
Acceptance Criteria:

✅ Unit tests pass for all Chat components
✅ Integration tests pass for useChat hook
✅ E2E test covers happy path (login→chat→send→response)
✅ Coverage report shows >70% coverage
✅ Tests run without errors: npm test
ISSUE #6: API ROUTE MISALIGNMENT (MAJOR)
Problem
Frontend calls: GET /api/{userId}/conversations
Backend provides: GET /api/v1/conversations/
Routes don't match → 404 errors
Frontend can't load conversation list
Root Cause
Prefix mismatch:

Chat router uses /api prefix
Conversation router uses /api/v1 prefix
Frontend expects unified /api/{userId}/ pattern
Solution Specification
Requirement 6.1: Standardize API Routes

Unified Route Structure:

All conversation/chat routes should follow pattern:

What to do:

Option 1: Move Everything to /api/{user_id} Pattern

Change conversation_router.py:

Option 2: Update Frontend Service Layer

Change chatService.ts to call correct backend routes:

Recommended Approach: Option 1 (Server)

Create clear user-scoped endpoints:

With user_id obtained from:

Better Auth session (via middleware)
OR request body parameter
NOT from URL path
Acceptance Criteria:

✅ Frontend service calls correct backend routes
✅ All responses return 200 (not 404)
✅ Conversation list loads on chat page
✅ Can navigate between conversations
✅ No CORS or route errors in console
ADDITIONAL REQUIREMENTS
Requirement 7: Environment Variables Documentation
Backend needs .env.example or documented variables:

Frontend already has .env.local:

Requirement 8: Error Handling Edge Cases
Backend chat endpoint must handle:

✅ Empty message → reject with 400
✅ Message too long (>10000 chars) → reject with 400
✅ Invalid user_id → reject with 400
✅ Non-existent conversation_id → reject with 404
✅ OpenAI API timeout → return 504 with retry message
✅ Tool execution fails → return error message with context
✅ Database error → return 500 with generic message
Frontend must handle:

✅ 401 Unauthorized → redirect to login
✅ 404 Not Found → show "Conversation not found"
✅ 500 Server Error → show "Server error, try again"
✅ Network timeout → show "Request timed out"
✅ Tool call fails → show which tool failed and why
Requirement 9: Conversation Title Generation
Backend should auto-generate conversation titles from first message:

Frontend displays title in sidebar instead of "None"

Requirement 10: Logging & Observability
Backend should log:

Every chat message sent (user_id, message length, conversation_id)
Tool execution (which tool, arguments, result status)
Errors (type, user_id, full traceback)
Performance (response time, tokens used)
Frontend should log:

Chat page load
Message send attempts
Errors (with user_id for debugging)
IMPLEMENTATION PRIORITY ORDER
BLOCKER (Do First - 30 mins):

Register chat router in main.py
Add chat button to home page
Test endpoints exist
CORE FEATURE (Next - 3-4 hours):

Implement tool execution loop
Test tool execution with database
Verify tasks created/updated/deleted
SPEC COMPLIANCE (Next - 2 hours):

Swap in @ai-sdk-react
Fix API route misalignment
Add conversation title generation
QUALITY (Final - 3-4 hours):

Write tests (unit + integration + E2E)
Add logging
Handle edge cases
TESTING ACCEPTANCE CRITERIA
Happy Path Test:

User logs in ✅
Navigates to Chat page ✅
Types "Add buy milk" ✅
Hits Enter → message sent ✅
Backend receives message ✅
AI identifies add_task tool ✅
Backend EXECUTES add_task ✅
Task created in database ✅
Response returned with tool result ✅
User sees "Task added: Buy milk (ID: 123)" ✅
User clicks "Show tasks" ✅
Backend executes list_tasks ✅
Shows "1. Buy milk [pending]" ✅
User refreshes page ✅
Conversation history loads ✅
All messages persist ✅
If ANY step fails → spec not met

DEFINITION OF DONE
✅ Chat endpoint registered and responding
✅ MCP tools execute and modify database
✅ Chat button visible on home page
✅ Using @ai-sdk-react for chat UI
✅ API routes unified and working
✅ Test coverage >70%
✅ All tool operations verified (add, list, complete, delete, update)
✅ Conversation history persists
✅ Error messages clear and helpful
✅ Mobile responsive
✅ Documentation updated

## RESPONSE_TEXT

Successfully created a comprehensive feature specification for fixing AI chatbot integration issues. The specification addresses the following critical issues:

1. Chat endpoint registration - ensuring the endpoint is accessible
2. MCP tool execution - enabling tools to modify the database as intended
3. Chatbot navigation - making the chat interface discoverable and accessible
4. ChatKit library compliance - ensuring proper UI library implementation
5. Test coverage - implementing comprehensive testing requirements
6. API route alignment - standardizing communication between frontend and backend

The specification includes detailed user scenarios with acceptance criteria, success metrics, functional requirements, key entities, technical architecture overview, assumptions, and decision points. It follows the spec-first approach and maintains focus on user value rather than implementation details. A quality checklist was created and validated to ensure the specification meets all requirements before proceeding to the planning phase.