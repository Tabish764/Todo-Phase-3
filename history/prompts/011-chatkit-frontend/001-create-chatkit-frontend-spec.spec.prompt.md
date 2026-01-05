---
id: "001"
title: "Create ChatKit Frontend UI Spec"
stage: "spec"
date_iso: "2025-12-29"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "011-chatkit-frontend"
branch: "011-chatkit-frontend"
user: "Claude Code"
command: "/sp.specify"
labels: ["specification", "frontend", "chatkit", "ui", "nextjs"]
links:
  spec: "specs/011-chatkit-frontend/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/011-chatkit-frontend/spec.md"
  - "specs/011-chatkit-frontend/checklists/requirements.md"
tests: []
---

# Prompt

```
/sp.specify # Feature Specification: Todo AI Chatbot - ChatKit Frontend UI

**Feature Branch**: \`011-chatkit-frontend\`
**Created**: 2025-12-27
**Status**: Draft
**Dependencies**:
- Feature 009: Chat API Endpoint (frontend sends requests here)
- Feature 010: AI Agent Configuration (provides intelligent responses)

## Overview

Build a Next.js frontend using OpenAI ChatKit component library that provides an intuitive, conversational interface for users to interact with the AI-powered todo chatbot. The interface must support new and existing conversations, display messages clearly, handle loading states, and integrate seamlessly with the FastAPI backend.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start New Conversation (Priority: P1)

As a user visiting the todo chatbot, I want to start a new conversation easily so that I can begin managing my tasks through AI assistance.

**Why this priority**: This is the entry point for all user interactions. Without the ability to start conversations, the chatbot is inaccessible.

**Independent Test**: Can be tested by clicking a "New Chat" button and verifying that the chat interface clears and is ready to accept the first message.

**Acceptance Scenarios**:

1. **Given** a user is on the chatbot page, **When** they click "New Chat" or arrive for the first time, **Then** an empty chat interface appears ready for input
2. **Given** a user types their first message in a new conversation, **When** they send it, **Then** a new conversation_id is created and the AI responds
3. **Given** the AI responds to the first message, **When** the conversation continues, **Then** subsequent messages use the same conversation_id

---

### User Story 2 - Send Messages and Receive Responses (Priority: P1)

As a user, I want to type natural language messages and receive timely AI responses so that I can have a fluid conversation about my tasks.

**Why this priority**: This is the core interaction pattern that enables all task management through conversation.

**Independent Test**: Can be tested by typing "Add buy milk" and verifying the message appears in the chat, a loading indicator shows, and an AI response arrives within seconds.

**Acceptance Scenarios**:

1. **Given** a user types a message in the input box, **When** they press Enter or click Send, **Then** the message appears in the chat as a user message
2. **Given** a message is sent, **When** the backend is processing, **Then** a loading indicator shows that the AI is thinking
3. **Given** the AI generates a response, **When** it arrives, **Then** it appears as an assistant message with proper formatting
4. **Given** the user is typing, **When** they press Shift+Enter, **Then** a new line is inserted without sending the message

---

### User Story 3 - View Conversation History (Priority: P2)

As a user with multiple conversations, I want to see a list of my recent chats and be able to resume any conversation so that I can continue where I left off.

**Why this priority**: This enables users to maintain multiple conversation threads and return to previous discussions about their tasks.

**Independent Test**: Can be tested by creating multiple conversations, then clicking on a previous conversation in the sidebar and verifying the full message history loads.

**Acceptance Scenarios**:

1. **Given** a user has multiple conversations, **When** they view the sidebar, **Then** they see a list of recent conversations sorted by most recent first
2. **Given** a user clicks on a conversation in the sidebar, **When** the conversation loads, **Then** all previous messages appear in chronological order
3. **Given** a conversation is loaded, **When** the user sends a new message, **Then** it continues the existing conversation rather than starting a new one
4. **Given** each conversation in the sidebar, **When** displayed, **Then** it shows a preview of the first or last message for context

---

### User Story 4 - Visual Message Differentiation (Priority: P2)

As a user having a conversation, I want to easily distinguish my messages from the AI's responses so that I can follow the conversation flow naturally.

**Why this priority**: Clear visual distinction prevents confusion and makes the interface feel like a natural conversation.

**Independent Test**: Can be tested by having a conversation and visually confirming that user and assistant messages are clearly differentiated by color, alignment, or styling.

**Acceptance Scenarios**:

1. **Given** messages are displayed, **When** viewing the chat, **Then** user messages appear with distinct styling (e.g., aligned right, different color)
2. **Given** messages are displayed, **When** viewing the chat, **Then** assistant messages appear with distinct styling (e.g., aligned left, different color)
3. **Given** each message is displayed, **When** viewing it, **Then** it includes a timestamp showing when it was sent
4. **Given** the AI makes tool calls, **When** viewing the message, **Then** optionally show which tools were invoked (expandable details)

---

### User Story 5 - Responsive Mobile Experience (Priority: P2)

As a mobile user, I want the chat interface to work well on my phone so that I can manage tasks on the go.

**Why this priority**: Many users access web applications primarily through mobile devices, so mobile support is essential for broad usability.

**Independent Test**: Can be tested by accessing the application on a mobile device or browser with mobile viewport and verifying all functionality works smoothly.

**Acceptance Scenarios**:

1. **Given** a user accesses the chatbot on mobile, **When** they view the interface, **Then** the layout adapts to the smaller screen size
2. **Given** a user is on mobile, **When** the sidebar is present, **Then** it collapses into a menu that can be toggled
3. **Given** a user types on mobile, **When** the keyboard appears, **Then** the input box remains accessible and the chat scrolls appropriately
4. **Given** messages are displayed on mobile, **When** scrolling, **Then** the interface performs smoothly without lag

---

### User Story 6 - Error Handling and User Feedback (Priority: P2)

As a user, when something goes wrong (network error, API failure), I want clear feedback about what happened and what I can do about it.

**Why this priority**: Good error handling prevents user frustration and helps users understand when to retry or seek help.

**Independent Test**: Can be tested by simulating network failures or API errors and verifying that appropriate error messages appear.

**Acceptance Scenarios**:

1. **Given** the backend is unreachable, **When** a user sends a message, **Then** an error message appears explaining the connection issue
2. **Given** the API returns an error, **When** the user sees it, **Then** the error message is user-friendly and actionable
3. **Given** a message fails to send, **When** the error appears, **Then** the user can retry sending the message
4. **Given** the user is typing, **When** they're waiting for a response, **Then** the input is disabled to prevent sending multiple requests

---

### User Story 7 - Auto-Scroll and Message Focus (Priority: P3)

As a user in an active conversation, I want the chat to automatically scroll to the latest message so that I don't have to manually scroll down after each exchange.

**Why this priority**: This creates a smooth, natural conversation flow and prevents users from losing track of where the conversation is.

**Independent Test**: Can be tested by sending multiple messages and verifying the chat automatically scrolls to show the latest message.

**Acceptance Scenarios**:

1. **Given** a new message arrives, **When** it appears in the chat, **Then** the view automatically scrolls to show the new message
2. **Given** a user scrolls up to read history, **When** they send a new message, **Then** the view scrolls back to the latest message
3. **Given** the chat has many messages, **When** loading a conversation, **Then** it scrolls to the bottom to show the most recent exchange

---

### Edge Cases

- What happens when a conversation has hundreds of messages (performance/loading)?
- How does the UI handle very long AI responses (multiple paragraphs)?
- What occurs when the user rapidly sends multiple messages before the first response arrives?
- How does the interface handle network disconnections mid-conversation?
- What happens when localStorage is disabled and conversation state cannot be cached?
- How does the UI handle messages with special characters, emojis, or markdown?
- What occurs when the OpenAI domain key is invalid or expired?
- How does the interface handle simultaneous conversations across multiple browser tabs?

---

## Requirements *(mandatory)*

### Functional Requirements

#### Chat Interface Components

- **FR-001**: Interface MUST display a message input box at the bottom of the screen
- **FR-002**: Interface MUST display a scrollable message history area above the input box
- **FR-003**: Interface MUST include a "Send" button next to the input box
- **FR-004**: Interface MUST include a "New Chat" button to start fresh conversations
- **FR-005**: Interface MUST show user messages aligned to the right with distinct styling
- **FR-006**: Interface MUST show assistant messages aligned to the left with distinct styling
- **FR-007**: Interface MUST display timestamps for each message
- **FR-008**: Interface MUST show a loading indicator while waiting for AI responses
- **FR-009**: Interface MUST disable input while a response is being generated
- **FR-010**: Interface MUST auto-scroll to the latest message when new messages arrive

#### Conversation Management

- **FR-011**: Interface MUST maintain a sidebar (or menu on mobile) listing recent conversations
- **FR-012**: Sidebar MUST display conversations sorted by most recent activity (updated_at)
- **FR-013**: Each conversation in sidebar MUST show a preview (first message or timestamp)
- **FR-014**: User MUST be able to click a conversation in sidebar to load its full history
- **FR-015**: User MUST be able to start a new conversation that creates a fresh conversation_id
- **FR-016**: Current conversation MUST be visually highlighted in the sidebar
- **FR-017**: Sidebar MUST collapse into a hamburger menu on mobile devices

#### Message Handling

- **FR-018**: User MUST be able to send messages by pressing Enter key
- **FR-019**: User MUST be able to create new lines by pressing Shift+Enter
- **FR-020**: User MUST be able to send messages by clicking the Send button
- **FR-021**: Empty messages MUST NOT be sent to the backend
- **FR-022**: Messages MUST be trimmed of leading/trailing whitespace before sending
- **FR-023**: System MUST prevent sending new messages while a response is pending
- **FR-024**: Long messages MUST wrap properly within the message bubble
- **FR-025**: Messages with markdown MUST be rendered appropriately (bold, italic, lists)

#### Backend Integration

- **FR-026**: Frontend MUST send POST requests to \`/api/{user_id}/chat\` endpoint
- **FR-027**: Frontend MUST include user_id in the API request path
- **FR-028**: Frontend MUST include message text in request body
- **FR-029**: Frontend MUST include conversation_id in request body for existing conversations
- **FR-030**: Frontend MUST NOT include conversation_id for new conversations
- **FR-031**: Frontend MUST handle 200 OK responses by displaying the AI's response
- **FR-032**: Frontend MUST extract conversation_id from response and use it for subsequent messages
- **FR-033**: Frontend MUST handle error responses (400, 401, 404, 500, 503) with appropriate user messages
- **FR-034**: Frontend MUST implement request timeout (e.g., 30 seconds) to prevent hanging
- **FR-035**: Frontend MUST retry failed requests once before showing error to user

#### OpenAI ChatKit Configuration

- **FR-036**: Frontend MUST use OpenAI ChatKit component library for the chat interface
- **FR-037**: Frontend MUST configure ChatKit with the OpenAI domain key from environment variables
- **FR-038**: Frontend MUST handle ChatKit initialization errors gracefully
- **FR-039**: Frontend MUST pass proper CORS headers when making requests to backend
- **FR-040**: Frontend MUST work with localhost during development without domain allowlist
- **FR-041**: Frontend MUST work with production domain after adding to OpenAI allowlist

#### State Management

- **FR-042**: Frontend MUST maintain current conversation_id in component state
- **FR-043**: Frontend MUST maintain message history in component state for current conversation
- **FR-044**: Frontend MUST track loading state to show/hide loading indicators
- **FR-045**: Frontend MUST track error state to display error messages
- **FR-046**: Frontend MUST clear state appropriately when starting a new conversation
- **FR-047**: Frontend MUST NOT use localStorage for conversation persistence (fetch from backend)

#### User Experience

- **FR-048**: Interface MUST be visually consistent with existing todo app design
- **FR-049**: Interface MUST use accessible color contrast ratios (WCAG AA minimum)
- **FR-050**: Interface MUST support keyboard navigation for accessibility
- **FR-051**: Interface MUST include ARIA labels on interactive elements
- **FR-052**: Interface MUST show focus indicators on focusable elements
- **FR-053**: Interface MUST be responsive and work on screen sizes from 320px to 4K
- **FR-054**: Interface MUST perform smoothly with 60fps scrolling
- **FR-055**: Interface MUST load within 3 seconds on 3G networks

#### Tool Call Display (Optional Enhancement)

- **FR-056**: Interface MAY show which MCP tools were called in each assistant message
- **FR-057**: Tool call details MAY be hidden by default and expandable on click
- **FR-058**: Tool call display SHOULD show tool name and key parameters
- **FR-059**: Tool call display SHOULD help users understand what actions the AI took

### Key Entities *(include if feature involves data)*

- **ChatMessage**: Display data for a single message including id, role (user/assistant), content, timestamp, and optional tool_calls
- **Conversation**: Metadata about a chat session including conversation_id, creation time, last updated time, and message count
- **ChatState**: Frontend state including current conversation_id, message array, loading status, error status, and input text
- **APIRequest**: Data structure for requests to backend including user_id, conversation_id, and message
- **APIResponse**: Data structure for responses from backend including conversation_id, response text, and tool_calls

---

## Technical Specifications

### Technology Stack

- **Framework**: Next.js (React-based)
- **Chat UI**: OpenAI ChatKit component library
- **Styling**: Tailwind CSS (or existing app's CSS framework)
- **State Management**: React hooks (useState, useEffect)
- **HTTP Client**: Fetch API or Axios
- **Type Safety**: TypeScript (recommended)

### Environment Variables

\`\`\`
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend API base URL
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-key      # OpenAI ChatKit domain key
NEXT_PUBLIC_USER_ID=user123                  # Current authenticated user (from auth)
\`\`\`

### Component Structure

**Main Chat Page Component:**
- Manages overall layout
- Contains sidebar and chat area
- Handles conversation switching
- Manages state for current conversation

**Message List Component:**
- Displays all messages in current conversation
- Auto-scrolls to latest message
- Handles different message types (user/assistant)

**Message Input Component:**
- Controlled input for message text
- Send button
- Enter/Shift+Enter handling
- Disabled state during loading

**Conversation Sidebar Component:**
- Lists recent conversations
- Highlights current conversation
- Handles conversation selection
- Collapses on mobile

**Loading Indicator Component:**
- Shows while AI is generating response
- Animated typing indicator or spinner

**Error Display Component:**
- Shows error messages
- Provides retry option
- Dismissible

### API Integration

**Sending Messages:**

\`\`\`javascript
// POST /api/{user_id}/chat
const response = await fetch(\`\${API_URL}/api/\${userId}/chat\`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    conversation_id: currentConversationId, // omit for new conversation
    message: userMessage.trim()
  })
});

const data = await response.json();
// data.conversation_id
// data.response
// data.tool_calls (optional)
\`\`\`

**Loading Conversations List:**

\`\`\`javascript
// GET /api/{user_id}/conversations
const response = await fetch(\`\${API_URL}/api/\${userId}/conversations\`);
const conversations = await response.json();
// Array of: { id, created_at, updated_at, last_message_preview }
\`\`\`

**Loading Conversation History:**

\`\`\`javascript
// GET /api/{user_id}/conversations/{conversation_id}/messages
const response = await fetch(\`\${API_URL}/api/\${userId}/conversations/\${conversationId}/messages\`);
const messages = await response.json();
// Array of: { id, role, content, tool_calls, created_at }
\`\`\`

### Message Display Format

**User Message:**
\`\`\`
┌─────────────────────────────────┐
│                                 │
│          Add buy milk       [You]│
│                     12:34 PM     │
└─────────────────────────────────┘
\`\`\`

**Assistant Message:**
\`\`\`
┌─────────────────────────────────┐
│[AI]                              │
│   I've added 'Buy milk' to your  │
│   task list!                     │
│                     12:34 PM     │
│   [Tools: add_task] (expandable) │
└─────────────────────────────────┘
\`\`\`

### State Management Pattern

\`\`\`javascript
const [currentConversationId, setCurrentConversationId] = useState(null);
const [messages, setMessages] = useState([]);
const [inputText, setInputText] = useState('');
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState(null);
const [conversations, setConversations] = useState([]);

// When user sends message:
const sendMessage = async (text) => {
  // Add user message to UI immediately
  const userMessage = { role: 'user', content: text, created_at: new Date() };
  setMessages([...messages, userMessage]);
  setInputText('');
  setIsLoading(true);

  try {
    const response = await fetch(...);
    const data = await response.json();

    // Update conversation_id if new conversation
    if (!currentConversationId) {
      setCurrentConversationId(data.conversation_id);
    }

    // Add assistant message to UI
    const assistantMessage = {
      role: 'assistant',
      content: data.response,
      tool_calls: data.tool_calls,
      created_at: new Date()
    };
    setMessages([...messages, userMessage, assistantMessage]);

  } catch (err) {
    setError('Failed to send message. Please try again.');
  } finally {
    setIsLoading(false);
  }
};
\`\`\`

### Responsive Design Breakpoints

- **Mobile**: < 768px
  - Sidebar collapses to hamburger menu
  - Full-width chat interface
  - Input box fixed at bottom

- **Tablet**: 768px - 1024px
  - Sidebar visible but narrower
  - Chat area takes remaining space

- **Desktop**: > 1024px
  - Sidebar at comfortable width (250-300px)
  - Chat area expands to fill space
  - Optimal reading width maintained

### OpenAI ChatKit Integration

**Setup Steps:**

1. Install ChatKit library: \`npm install @openai/chatkit\`

2. Configure domain allowlist:
   - Deploy frontend to production URL
   - Add domain to: https://platform.openai.com/settings/organization/security/domain-allowlist
   - Obtain domain key

3. Initialize ChatKit:
\`\`\`javascript
import { ChatKit } from '@openai/chatkit';

<ChatKit
  domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY}
  onSendMessage={handleSendMessage}
  messages={messages}
  isLoading={isLoading}
/>
\`\`\`

**Note**: Localhost works without domain allowlist during development

### Error Handling Patterns

**Network Errors:**
- Display: "Connection error. Check your internet and try again."
- Action: Provide retry button

**400 Bad Request:**
- Display: "Invalid message. Please try again."
- Action: Allow user to edit and resend

**401 Unauthorized:**
- Display: "You're not logged in. Please sign in to continue."
- Action: Redirect to login

**404 Not Found:**
- Display: "This conversation no longer exists."
- Action: Redirect to new conversation

**500 Server Error:**
- Display: "Something went wrong on our end. Please try again."
- Action: Provide retry button

**503 Service Unavailable:**
- Display: "Service is temporarily unavailable. Please try again in a moment."
- Action: Automatic retry after 5 seconds

### Performance Optimization

- **Message Virtualization**: For conversations with 100+ messages, render only visible messages
- **Lazy Loading**: Load conversation list progressively
- **Debouncing**: Debounce input to prevent excessive re-renders
- **Image Optimization**: Use Next.js Image component if showing any images
- **Code Splitting**: Lazy load ChatKit component to reduce initial bundle size

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can send a message and receive a response in 100% of successful cases
- **SC-002**: Interface responds to user input within 100ms (typing, clicking)
- **SC-003**: Messages display within 200ms of receiving API response
- **SC-004**: Auto-scroll to latest message works in 100% of cases
- **SC-005**: Sidebar correctly lists all user conversations sorted by recency
- **SC-006**: Clicking a conversation loads its full history within 2 seconds
- **SC-007**: New conversation button clears interface and starts fresh in 100% of cases
- **SC-008**: Enter key sends message in 100% of cases
- **SC-009**: Shift+Enter creates new line in 100% of cases
- **SC-010**: Interface prevents sending empty or whitespace-only messages
- **SC-011**: Loading indicator displays during AI response generation
- **SC-012**: Error messages appear for all API failure scenarios
- **SC-013**: Interface works on mobile devices (320px+ width)
- **SC-014**: Interface works on desktop devices (1920px+ width)
- **SC-015**: ChatKit integration works with proper domain key configuration

### Quality Metrics

- **QM-001**: First Contentful Paint under 1.5 seconds
- **QM-002**: Time to Interactive under 3 seconds
- **QM-003**: Cumulative Layout Shift under 0.1
- **QM-004**: Lighthouse Accessibility score 90+
- **QM-005**: No console errors during normal operation

### Testing Requirements

- **TR-001**: Unit tests for message sending logic
- **TR-002**: Unit tests for conversation switching logic
- **TR-003**: Integration tests for API communication
- **TR-004**: Integration tests for ChatKit component integration
- **TR-005**: E2E tests for complete conversation flow (start to finish)
- **TR-006**: E2E tests for error scenarios
- **TR-007**: Responsive design tests on multiple viewport sizes
- **TR-008**: Accessibility tests with keyboard navigation
- **TR-009**: Performance tests with long conversations (100+ messages)
- **TR-010**: Cross-browser tests (Chrome, Firefox, Safari, Edge)
```

# Response

Successfully created the specification for the ChatKit Frontend UI feature. The specification includes:

1. A comprehensive feature overview
2. 7 detailed user stories with acceptance scenarios
3. A complete list of functional requirements (FR-001 to FR-059)
4. Definition of key entities involved in the feature
5. Technical specifications including component structure and API integration
6. Success criteria with measurable outcomes (SC-001 to SC-015) and quality metrics
7. Testing requirements (TR-001 to TR-010)

The specification follows the required template structure and includes all mandatory sections. It defines a Next.js frontend using OpenAI ChatKit that integrates with the existing AI backend to provide a conversational todo chatbot interface.

A quality checklist was also created to validate that the specification meets all requirements before proceeding to the planning phase.

The feature branch '011-chatkit-frontend' was created and the specification is ready for the next phase of development.

# Outcome

The ChatKit Frontend UI feature specification is complete and ready for planning. The specification covers all aspects of the conversational interface including conversation management, message display, mobile responsiveness, and error handling. The next step would be to run /sp.plan to create the implementation plan.