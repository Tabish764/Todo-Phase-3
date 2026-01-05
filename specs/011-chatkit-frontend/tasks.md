# Implementation Tasks: Todo AI Chatbot - ChatKit Frontend UI

## Phase 1: Setup & Dependencies
- [x] T1P1 Verify Next.js project structure with TypeScript, Tailwind CSS, and ESLint `frontend/`
- [x] T1P2 Install OpenAI ChatKit package (`@ai-sdk/react` or `@openai/chatkit`) `frontend/package.json`
- [x] T1P3 Configure environment variables for API and ChatKit `.env.local`
  - `NEXT_PUBLIC_API_URL=http://localhost:8000`
  - `NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key` (optional for localhost)
  - Verify Better Auth variables exist
- [x] T1P4 Verify TypeScript settings and path aliases (`@"/*"`) `frontend/tsconfig.json`
- [x] T1P5 Create project structure for chat components `frontend/src/components/Chat/`
- [x] T1P6 Document domain allowlist setup for production `README.md`

## Phase 2: Core Types & Services
- [x] T2P1 Create chat-related TypeScript types `frontend/src/types/chat.ts`
  - `Message`, `ChatRequest`, `ChatResponse`, `ToolCall` interfaces
  - Align with backend response models
- [x] T2P2 Implement chat service layer for backend API `frontend/src/services/chatService.ts`
  - `sendMessage(userId, request)` method
  - Error handling and response parsing
  - Integration with existing `apiClient`
- [x] T2P3 Create conversation service (if needed) `frontend/src/services/conversationService.ts`
  - `getConversations(userId)` - list user's conversations
  - `getConversationHistory(userId, conversationId)` - if backend provides endpoint
- [x] T2P4 Verify Better Auth integration `frontend/src/lib/auth-client.ts`
  - Ensure `useAuth()` hook provides `user.id`
  - Verify session token retrieval works

## Phase 3: Chat Hook & State Management
- [x] T3P1 Create `useChat` custom hook `frontend/src/hooks/useChat.ts`
  - State: `messages`, `conversationId`, `isLoading`, `error`
  - Methods: `sendMessage(content)`, `startNewConversation()`
  - Integration with `chatService`
- [x] T3P2 Add conversation loading logic to hook `frontend/src/hooks/useChat.ts`
  - Load conversation history when `conversationId` changes
  - Handle new vs existing conversations
- [x] T3P3 Add error handling to hook `frontend/src/hooks/useChat.ts`
  - Network errors, API errors, timeout handling
  - Error state management

## Phase 4: ChatKit Component Integration
- [x] T4P1 Create ChatKit wrapper component `frontend/src/components/Chat/ChatKitWrapper.tsx`
  - Integrate `@ai-sdk/react` `useChat` hook OR custom implementation
  - Connect to backend via `chatService`
  - Display messages from `useChat` hook
- [x] T4P2 Implement message display in ChatKit `frontend/src/components/Chat/ChatKitWrapper.tsx`
  - User messages styling
  - Assistant messages styling
  - Loading indicator during AI processing
- [x] T4P3 Add message input handling `frontend/src/components/Chat/ChatKitWrapper.tsx`
  - Send on Enter, new line on Shift+Enter
  - Disable input while loading
  - Clear input after send
- [x] T4P4 Integrate with `useChat` hook `frontend/src/components/Chat/ChatKitWrapper.tsx`
  - Pass `messages`, `sendMessage`, `isLoading` from hook
  - Handle errors from hook

## Phase 5: Chat Page Route
- [x] T5P1 Create chat page route `frontend/src/app/chat/page.tsx`
  - Client component with authentication check
  - Redirect to login if not authenticated
- [x] T5P2 Integrate ChatKit wrapper in page `frontend/src/app/chat/page.tsx`
  - Use `useAuth()` to get user ID
  - Use `useChat()` hook
  - Pass props to `ChatKitWrapper`
- [x] T5P3 Add loading states `frontend/src/app/chat/page.tsx`
  - Show loading while checking authentication
  - Show loading while initializing chat
- [x] T5P4 Add error boundaries `frontend/src/app/chat/page.tsx`
  - Catch and display errors gracefully

## Phase 6: Conversation Sidebar (P2)
- [x] T6P1 Create conversation sidebar component `frontend/src/components/Chat/ConversationSidebar.tsx`
  - List of user's conversations
  - "New Chat" button
  - Current conversation highlight
- [x] T6P2 Implement conversation list fetching `frontend/src/components/Chat/ConversationSidebar.tsx`
  - Call backend to get user's conversations (if endpoint exists)
  - Or manage locally in state
- [x] T6P3 Add conversation selection `frontend/src/components/Chat/ConversationSidebar.tsx`
  - Click conversation to load it
  - Update `conversationId` in `useChat` hook
- [x] T6P4 Add conversation preview `frontend/src/components/Chat/ConversationSidebar.tsx`
  - Show first/last message preview
  - Show timestamp
- [x] T6P5 Make sidebar responsive `frontend/src/components/Chat/ConversationSidebar.tsx`
  - Collapsible on mobile
  - Toggle button for mobile

## Phase 7: Tool Call Visualization (P2)
- [x] T7P1 Create tool call display component `frontend/src/components/Chat/ToolCallDisplay.tsx`
  - Display tool name and arguments
  - Show tool execution result (if available)
  - Expandable/collapsible details
- [x] T7P2 Integrate tool call display in messages `frontend/src/components/Chat/ChatKitWrapper.tsx`
  - Show tool calls in assistant messages
  - Optional: inline or expandable
- [x] T7P3 Style tool call visualization `frontend/src/components/Chat/ToolCallDisplay.tsx`
  - Distinct styling from regular messages
  - Icons for different tool types

## Phase 8: Error Handling & User Feedback
- [x] T8P1 Create error display component `frontend/src/components/Chat/ErrorDisplay.tsx`
  - Display error messages
  - Retry button for failed requests
  - Different styles for different error types
- [x] T8P2 Integrate error display in chat `frontend/src/components/Chat/ChatKitWrapper.tsx`
  - Show errors from `useChat` hook
  - Handle 401 (redirect to login)
  - Handle 500 (show retry)
  - Handle network errors
- [x] T8P3 Add retry functionality `frontend/src/components/Chat/ErrorDisplay.tsx`
  - Retry failed message sends
  - Clear error on retry
- [x] T8P4 Add timeout handling `frontend/src/hooks/useChat.ts`
  - Detect slow responses
  - Show timeout message
  - Allow cancellation

## Phase 9: Conversation Persistence
- [x] T9P1 Implement conversation ID management `frontend/src/hooks/useChat.ts`
  - Store `conversationId` in state
  - Update when new conversation starts
  - Update when loading existing conversation
- [x] T9P2 Add URL parameter support `frontend/src/app/chat/page.tsx`
  - Support `/chat?conversation_id=123`
  - Load conversation on page load
- [x] T9P3 Persist conversation ID in URL `frontend/src/app/chat/page.tsx`
  - Update URL when conversation changes
  - Browser back/forward support
- [x] T9P4 Handle page refresh `frontend/src/app/chat/page.tsx`
  - Restore conversation from URL parameter
  - Load conversation history on mount

## Phase 10: Mobile Responsiveness
- [x] T10P1 Make chat interface responsive `frontend/src/components/Chat/ChatKitWrapper.tsx`
  - Mobile-friendly message display
  - Touch-friendly input
  - Proper keyboard handling
- [x] T10P2 Make sidebar mobile-friendly `frontend/src/components/Chat/ConversationSidebar.tsx`
  - Collapsible drawer on mobile
  - Overlay on mobile
  - Toggle button
- [x] T10P3 Optimize for mobile performance `frontend/src/app/chat/page.tsx`
  - Lazy load components
  - Optimize re-renders
  - Smooth scrolling

## Phase 11: Polish & Accessibility
- [x] T11P1 Add accessibility features `frontend/src/components/Chat/*.tsx`
  - ARIA labels for buttons and inputs
  - Keyboard navigation support
  - Screen reader support
- [x] T11P2 Add loading skeletons `frontend/src/components/Chat/LoadingIndicator.tsx`
  - Skeleton for messages while loading
  - Skeleton for conversation list
- [x] T11P3 Add smooth animations `frontend/src/components/Chat/*.tsx`
  - Message appearance animation
  - Loading state transitions
- [x] T11P4 Add auto-scroll to latest message `frontend/src/components/Chat/ChatKitWrapper.tsx`
  - Scroll to bottom on new message
  - Smooth scroll behavior

## Phase 12: Testing & Documentation
- [x] T12P1 Write unit tests for chat service `frontend/src/services/__tests__/chatService.test.ts`
- [x] T12P2 Write unit tests for useChat hook `frontend/src/hooks/__tests__/useChat.test.ts`
- [x] T12P3 Write integration tests `frontend/src/app/chat/__tests__/chat.test.tsx`
- [x] T12P4 Update README with ChatKit setup `frontend/README.md`
  - Installation instructions
  - Environment variables
  - Domain allowlist setup
- [x] T12P5 Document API integration `frontend/docs/chat-integration.md`
  - Backend endpoint details
  - Request/response formats
  - Error handling

## Dependency Graph
```
T1 (Setup) → T2 (Types & Services)
T2 → T3 (Chat Hook)
T3 → T4 (ChatKit Integration)
T4 → T5 (Chat Page)
T2 → T6 (Sidebar) [can run parallel with T4]
T4 → T7 (Tool Calls) [can run parallel with T6]
T3 → T8 (Error Handling) [can run parallel with T4]
T5 → T9 (Persistence) [can run parallel with T6]
T4, T6 → T10 (Mobile) [can run parallel]
T4, T6, T7, T8 → T11 (Polish) [can run parallel]
All → T12 (Testing) [final phase]
```

## Parallel Execution Examples
- Phase 2: T2P1, T2P2, T2P3, T2P4 can run in parallel
- Phase 4: T4P1, T4P2, T4P3 can run in parallel
- Phase 6: T6P1, T6P2, T6P3 can run in parallel
- Phase 7: T7P1, T7P2, T7P3 can run in parallel
- Phase 8: T8P1, T8P2, T8P3 can run in parallel

## Critical Path
1. T1P2 (Install ChatKit) - **BLOCKER**
2. T2P2 (Chat Service) - **BLOCKER**
3. T3P1 (useChat Hook) - **BLOCKER**
4. T4P1 (ChatKit Wrapper) - **BLOCKER**
5. T5P1 (Chat Page) - **BLOCKER**

These must be completed in order before other features can be built.

## Notes
- **ChatKit Package**: Verify which package to use - `@ai-sdk/react` (Vercel AI SDK) or OpenAI's official ChatKit package
- **Backend Integration**: Backend handles conversation history internally, so frontend mainly needs to pass `conversation_id`
- **Authentication**: Must use Better Auth session token in API requests
- **Domain Allowlist**: Only needed for production deployment, not localhost development
