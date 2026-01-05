# Feature Specification: Todo AI Chatbot - OpenAI ChatKit Frontend

**Feature Branch**: `011-chatkit-frontend`
**Created**: 2025-01-XX
**Status**: Draft
**Dependencies**:
- Feature 009: Chat API Endpoint (`POST /api/{user_id}/chat`)
- Feature 006: Better Auth Integration (for user authentication)
- Backend running on `http://localhost:8000`

## Overview

Build a Next.js frontend using **OpenAI ChatKit** component library that provides a conversational interface for users to interact with the AI-powered todo chatbot. The interface integrates with the existing FastAPI backend chat endpoint, uses Better Auth for authentication, and provides a seamless chat experience with conversation management.

**Key Requirements:**
- Use OpenAI ChatKit (not custom chat components)
- Integrate with backend `/api/{user_id}/chat` endpoint
- Use Better Auth for user authentication
- Support conversation persistence and history
- Display tool calls and AI responses
- Responsive design for mobile and desktop

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend Framework | Next.js 16+ (App Router) |
| Chat UI Library | OpenAI ChatKit (`@ai-sdk/react` or OpenAI ChatKit package) |
| Authentication | Better Auth (existing) |
| API Client | Custom service layer for backend communication |
| Styling | Tailwind CSS (existing) |
| TypeScript | Full type safety |

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authenticated Chat Access (Priority: P1)

As an authenticated user, I want to access the chat interface so that I can manage my tasks through conversation.

**Why this priority**: Users must be authenticated to use the chat, as the backend requires `user_id` and session tokens.

**Independent Test**: Can be tested by logging in, navigating to `/chat`, and verifying the chat interface loads with the user's ID.

**Acceptance Scenarios**:

1. **Given** a user is not logged in, **When** they try to access `/chat`, **Then** they are redirected to `/login`
2. **Given** a user is logged in, **When** they navigate to `/chat`, **Then** the chat interface loads with their user ID from Better Auth session
3. **Given** a user's session expires, **When** they try to send a message, **Then** they are redirected to login with a clear error message

---

### User Story 2 - Start New Conversation (Priority: P1)

As a user, I want to start a new conversation easily so that I can begin managing my tasks through AI assistance.

**Why this priority**: This is the entry point for all user interactions.

**Independent Test**: Can be tested by clicking "New Chat" and verifying the chat interface clears and is ready for the first message.

**Acceptance Scenarios**:

1. **Given** a user is on the chat page, **When** they click "New Chat" or arrive for the first time, **Then** an empty chat interface appears ready for input
2. **Given** a user types their first message in a new conversation, **When** they send it, **Then** the backend creates a new conversation_id and the AI responds
3. **Given** the AI responds to the first message, **When** the conversation continues, **Then** subsequent messages use the same conversation_id

---

### User Story 3 - Send Messages and Receive AI Responses (Priority: P1)

As a user, I want to type natural language messages and receive timely AI responses so that I can have a fluid conversation about my tasks.

**Why this priority**: This is the core interaction pattern that enables all task management through conversation.

**Independent Test**: Can be tested by typing "Add buy milk" and verifying the message appears, a loading indicator shows, and an AI response arrives.

**Acceptance Scenarios**:

1. **Given** a user types a message in ChatKit input, **When** they press Enter or click Send, **Then** the message appears in the chat as a user message
2. **Given** a message is sent, **When** the backend is processing, **Then** ChatKit shows a loading indicator that the AI is thinking
3. **Given** the AI generates a response, **When** it arrives from the backend, **Then** it appears as an assistant message with proper formatting
4. **Given** the user sends "Add a task to buy groceries", **When** the AI processes it, **Then** the add_task MCP tool is called and the response confirms the task was created

---

### User Story 4 - Conversation History Persistence (Priority: P1)

As a user, I want my conversation history to persist across sessions so that I can resume conversations and the AI maintains context.

**Why this priority**: This enables the AI to understand references to previous messages and allows users to resume conversations.

**Independent Test**: Can be tested by having a conversation, refreshing the page, and verifying all messages reload from the backend.

**Acceptance Scenarios**:

1. **Given** a user has an existing conversation, **When** they navigate to `/chat?conversation_id=123`, **Then** all previous messages load from the backend and display in chronological order
2. **Given** a user refreshes the page mid-conversation, **When** the page reloads, **Then** the conversation history is restored from the backend
3. **Given** a user sends a new message in an existing conversation, **When** it's processed, **Then** it continues the existing conversation rather than starting a new one

---

### User Story 5 - View Conversation List (Priority: P2)

As a user with multiple conversations, I want to see a list of my recent chats and be able to switch between them.

**Why this priority**: This enables users to maintain multiple conversation threads and return to previous discussions.

**Independent Test**: Can be tested by creating multiple conversations, then clicking on a previous conversation in the sidebar and verifying it loads.

**Acceptance Scenarios**:

1. **Given** a user has multiple conversations, **When** they view the sidebar, **Then** they see a list of recent conversations sorted by most recent first
2. **Given** a user clicks on a conversation in the sidebar, **When** the conversation loads, **Then** all previous messages appear in chronological order
3. **Given** each conversation in the sidebar, **When** displayed, **Then** it shows a preview of the first or last message for context

---

### User Story 6 - Tool Call Visualization (Priority: P2)

As a user, I want to see when the AI uses tools to manage my tasks so that I understand what actions were taken.

**Why this priority**: Transparency about tool usage helps users understand what the AI is doing behind the scenes.

**Independent Test**: Can be tested by sending "Show my tasks" and verifying that tool calls are displayed or indicated in the response.

**Acceptance Scenarios**:

1. **Given** the AI calls an MCP tool, **When** the response arrives, **Then** the tool_calls array is available in the response
2. **Given** tool calls are present, **When** displaying the message, **Then** optionally show which tools were invoked (expandable details or inline)
3. **Given** a tool call fails, **When** the error occurs, **Then** a user-friendly error message is displayed

---

### User Story 7 - Error Handling and User Feedback (Priority: P2)

As a user, I want clear error messages when something goes wrong so that I understand what happened and can take appropriate action.

**Why this priority**: Good error handling ensures users aren't left confused when failures occur.

**Independent Test**: Can be tested by simulating network failures or invalid requests and verifying appropriate error messages.

**Acceptance Scenarios**:

1. **Given** the backend returns a 401 error, **When** it occurs, **Then** the user is redirected to login with a clear message
2. **Given** the backend returns a 500 error, **When** it occurs, **Then** a user-friendly error message is displayed with a retry option
3. **Given** the network connection is lost, **When** sending a message, **Then** a network error message is shown with retry functionality
4. **Given** the backend takes too long to respond, **When** a timeout occurs, **Then** a timeout message is shown with retry option

---

### User Story 8 - Responsive Mobile Experience (Priority: P2)

As a mobile user, I want the chat interface to work well on my phone so that I can manage tasks on the go.

**Why this priority**: Many users access web applications primarily through mobile devices.

**Independent Test**: Can be tested by accessing the application on a mobile device and verifying all functionality works smoothly.

**Acceptance Scenarios**:

1. **Given** a user accesses the chatbot on mobile, **When** they view the interface, **Then** ChatKit adapts to the smaller screen size
2. **Given** a user is on mobile, **When** the sidebar is present, **Then** it collapses into a menu that can be toggled
3. **Given** a user types on mobile, **When** the keyboard appears, **Then** the input box remains accessible and the chat scrolls appropriately

---

## Technical Architecture

### Component Structure

```
frontend/src/
├── app/
│   └── chat/
│       └── page.tsx                    # Main chat page route
├── components/
│   └── Chat/
│       ├── ChatKitWrapper.tsx          # ChatKit component wrapper
│       ├── ConversationSidebar.tsx    # Conversation list sidebar
│       └── ErrorDisplay.tsx            # Error message component
├── services/
│   ├── chatService.ts                  # Chat API service
│   └── conversationService.ts          # Conversation management
├── hooks/
│   └── useChat.ts                      # Chat state management hook
├── lib/
│   ├── auth-client.ts                  # Better Auth client (existing)
│   └── api.ts                          # API client (existing)
└── types/
    └── chat.ts                         # TypeScript types
```

### Data Flow

```
User Input (ChatKit)
    ↓
useChat Hook
    ↓
chatService.sendMessage()
    ↓
Backend API: POST /api/{user_id}/chat
    ↓
Backend processes with AI Agent + MCP Tools
    ↓
Response: { conversation_id, response, tool_calls }
    ↓
ChatKit displays response
    ↓
Conversation persisted in database (backend)
```

---

## API Integration

### Backend Chat Endpoint

**Endpoint**: `POST /api/{user_id}/chat`

**Request**:
```typescript
interface ChatRequest {
  conversation_id?: number;  // Optional: null for new conversation
  message: string;           // Required: user's message
}
```

**Response**:
```typescript
interface ChatResponse {
  conversation_id: number;   // ID of the conversation
  response: string;          // AI's text response
  tool_calls?: ToolCall[];  // Optional: MCP tools that were called
}

interface ToolCall {
  tool_name: string;         // e.g., "add_task", "list_tasks"
  arguments: Record<string, any>;  // Tool parameters
  result: Record<string, any>;      // Tool execution result
}
```

### Authentication

- Use Better Auth session token in `Authorization: Bearer <token>` header
- Get user ID from Better Auth session: `session.user.id`
- Handle 401 errors by redirecting to login

---

## OpenAI ChatKit Integration

### Installation

```bash
npm install @ai-sdk/react
# OR if OpenAI provides a specific ChatKit package:
npm install @openai/chatkit
```

### Configuration

**Environment Variables** (`.env.local`):
```env
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# OpenAI ChatKit (if required)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here

# Better Auth (existing)
BETTER_AUTH_URL=http://localhost:3000
```

### ChatKit Component Usage

**Option 1: Using @ai-sdk/react (Recommended)**
```typescript
import { useChat } from '@ai-sdk/react';

function ChatInterface() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',  // Custom API route that proxies to backend
    body: {
      user_id: userId,
      conversation_id: currentConversationId,
    },
  });

  return (
    <div>
      {messages.map((message) => (
        <div key={message.id}>
          {message.role}: {message.content}
        </div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

**Option 2: Custom Integration with Backend**
```typescript
// Custom hook that integrates ChatKit with your backend
function useChatWithBackend(userId: string, conversationId?: number) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (content: string) => {
    setIsLoading(true);
    try {
      const response = await chatService.sendMessage({
        user_id: userId,
        conversation_id: conversationId,
        message: content,
      });
      
      // Add user message
      setMessages(prev => [...prev, { role: 'user', content }]);
      
      // Add assistant response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.response,
        tool_calls: response.tool_calls,
      }]);
      
      // Update conversation ID if new
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
      }
    } catch (error) {
      // Handle error
    } finally {
      setIsLoading(false);
    }
  };

  return { messages, sendMessage, isLoading };
}
```

---

## Implementation Details

### 1. Chat Service Layer

**File**: `frontend/src/services/chatService.ts`

```typescript
import { apiClient } from '@/lib/api';

export interface SendMessageRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls?: Array<{
    tool_name: string;
    arguments: Record<string, any>;
    result: Record<string, any>;
  }>;
}

export class ChatService {
  async sendMessage(
    userId: string,
    request: SendMessageRequest
  ): Promise<ChatResponse> {
    const response = await apiClient.request<ChatResponse>(
      `/api/${userId}/chat`,
      {
        method: 'POST',
        body: JSON.stringify(request),
      }
    );

    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to send message');
    }

    return response.data;
  }

  async getConversationHistory(
    userId: string,
    conversationId: number
  ): Promise<Message[]> {
    // This would call a backend endpoint to get conversation history
    // For now, the chat endpoint loads history internally
    // You may need to add: GET /api/{user_id}/conversations/{conversation_id}/messages
    throw new Error('Not implemented - backend handles history internally');
  }
}

export const chatService = new ChatService();
```

### 2. Chat Hook

**File**: `frontend/src/hooks/useChat.ts`

```typescript
import { useState, useCallback } from 'react';
import { chatService } from '@/services/chatService';
import { useAuth } from '@/lib/auth-client';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  tool_calls?: Array<{
    tool_name: string;
    arguments: Record<string, any>;
    result: Record<string, any>;
  }>;
  timestamp: Date;
}

export function useChat() {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    if (!user?.id) {
      setError('User not authenticated');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await chatService.sendMessage(user.id, {
        conversation_id: conversationId || undefined,
        message: content,
      });

      // Add user message
      const userMessage: Message = {
        id: `user-${Date.now()}`,
        role: 'user',
        content,
        timestamp: new Date(),
      };

      // Add assistant response
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
      role: 'assistant',
        content: response.response,
        tool_calls: response.tool_calls,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, userMessage, assistantMessage]);
      
      // Update conversation ID if new
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
      }
  } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
  } finally {
    setIsLoading(false);
  }
  }, [user?.id, conversationId]);

  const startNewConversation = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
  }, []);

  return {
    messages,
    sendMessage,
    isLoading,
    error,
    conversationId,
    startNewConversation,
  };
}
```

### 3. Chat Page Component

**File**: `frontend/src/app/chat/page.tsx`

```typescript
'use client';

import { useAuth } from '@/lib/auth-client';
import { useChat } from '@/hooks/useChat';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import ChatKitWrapper from '@/components/Chat/ChatKitWrapper';
import ConversationSidebar from '@/components/Chat/ConversationSidebar';

export default function ChatPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const chat = useChat();

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  if (authLoading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return null; // Will redirect
  }

  return (
    <div className="flex h-screen">
      <ConversationSidebar
        userId={user.id}
        currentConversationId={chat.conversationId}
        onSelectConversation={(id) => {
          // Load conversation history
          chat.loadConversation(id);
        }}
        onNewConversation={chat.startNewConversation}
      />
      <div className="flex-1 flex flex-col">
        <ChatKitWrapper
          messages={chat.messages}
          onSendMessage={chat.sendMessage}
          isLoading={chat.isLoading}
          error={chat.error}
        />
      </div>
    </div>
  );
}
```

---

## Error Handling

### Error Types

1. **Authentication Errors (401)**
   - Redirect to `/login`
   - Show message: "Please log in to continue"

2. **Network Errors**
   - Show: "Connection error. Check your internet and try again."
   - Provide retry button

3. **Validation Errors (400)**
   - Show: "Invalid message. Please try again."
   - Allow user to edit and resend

4. **Server Errors (500)**
   - Show: "Something went wrong on our end. Please try again."
   - Provide retry button

5. **Timeout Errors**
   - Show: "Request timed out. Please try again."
   - Provide retry button

---

## Testing Strategy

### Unit Tests
- Chat service API calls
- Chat hook state management
- Message formatting
- Error handling

### Integration Tests
- Full message send/receive flow
- Conversation persistence
- Authentication flow
- Error scenarios

### E2E Tests
- Complete user journey: login → chat → send message → receive response
- Multiple conversations
- Tool call visualization
- Mobile responsiveness

---

## Deployment Considerations

### Domain Allowlist (Production)

1. Deploy frontend to production (Vercel, etc.)
2. Get production URL: `https://your-app.vercel.app`
3. Add domain to OpenAI: https://platform.openai.com/settings/organization/security/domain-allowlist
4. Obtain domain key
5. Set `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` in production environment

**Note**: Localhost works without domain allowlist during development.

---

## Success Criteria

✅ User can log in and access chat interface
✅ User can send messages and receive AI responses
✅ Conversations persist across page refreshes
✅ Tool calls are visible (optional visualization)
✅ Error handling works for all scenarios
✅ Mobile responsive design
✅ Integration with existing Better Auth
✅ Integration with backend `/api/{user_id}/chat` endpoint

---

## Dependencies & Prerequisites

- ✅ Backend chat endpoint running on `http://localhost:8000`
- ✅ Better Auth configured and working
- ✅ User authentication flow established
- ✅ OpenAI API key configured (backend)
- ✅ ChatKit package installed (`@ai-sdk/react` or equivalent)

---

## Open Questions / Decisions Needed

1. **ChatKit Package**: Which exact package to use?
   - `@ai-sdk/react` (Vercel AI SDK)
   - `@openai/chatkit` (if exists)
   - Custom implementation with ChatKit-like UI

2. **Conversation History Loading**: 
   - Does backend provide `GET /api/{user_id}/conversations/{id}/messages`?
   - Or should frontend rely on backend loading history internally?

3. **Tool Call Display**:
   - Show inline in message?
   - Expandable details?
   - Separate component?

4. **Real-time Updates**:
   - Polling for new messages?
   - WebSocket (future)?
   - Current: Request/response only

---

## Next Steps

1. Install ChatKit package
2. Create chat service layer
3. Create chat hook
4. Build chat page component
5. Integrate with Better Auth
6. Test end-to-end flow
7. Add error handling
8. Add conversation sidebar
9. Polish UI/UX
10. Deploy and configure domain allowlist
