# Quickstart: Todo AI Chatbot - ChatKit Frontend UI

## Overview
Quickstart guide for setting up and running the ChatKit Frontend UI for the Todo AI Chatbot.

## Prerequisites
- Node.js 18+ and npm/yarn/pnpm
- Backend API running on `http://localhost:8000` (from Feature 009: Chat API Endpoint)
- Better Auth configured and working
- User account created and able to log in
- OpenAI API key configured in backend (for AI responses)

## Setup Instructions

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies

**Install OpenAI ChatKit Package:**
```bash
# Option 1: Vercel AI SDK (Recommended)
npm install ai @ai-sdk/react

# Option 2: If OpenAI provides official ChatKit package
npm install @openai/chatkit
```

**Verify existing dependencies:**
```bash
npm install
```

### 3. Environment Configuration

Create or update `.env.local` file in the `frontend` directory:

```env
# Backend API configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# OpenAI ChatKit configuration (optional for localhost)
# Only needed for production deployment
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here

# Better Auth configuration (should already exist)
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-here
```

**Note**: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` is only required for production. Localhost works without it.

### 4. Verify Backend is Running

Ensure your backend is running and accessible:
```bash
# In backend directory
uvicorn src.main:app --reload

# Test backend endpoint
curl http://localhost:8000/health
```

### 5. Start Development Server

```bash
# In frontend directory
npm run dev
```

The application should start on `http://localhost:3000`

### 6. Test the Chat Interface

1. **Navigate to Login**: `http://localhost:3000/login`
2. **Log in** with your credentials
3. **Navigate to Chat**: `http://localhost:3000/chat`
4. **Send a test message**: "Add a task to buy groceries"
5. **Verify response**: You should receive an AI response and the task should be created

## Project Structure

After implementation, your structure should look like:

```
frontend/
├── src/
│   ├── app/
│   │   └── chat/
│   │       └── page.tsx              # Main chat page
│   ├── components/
│   │   └── Chat/
│   │       ├── ChatKitWrapper.tsx    # ChatKit component
│   │       ├── ConversationSidebar.tsx
│   │       ├── ErrorDisplay.tsx
│   │       └── ToolCallDisplay.tsx
│   ├── services/
│   │   ├── chatService.ts            # Backend API integration
│   │   └── conversationService.ts
│   ├── hooks/
│   │   └── useChat.ts                # Chat state management
│   ├── lib/
│   │   ├── auth-client.ts            # Better Auth (existing)
│   │   └── api.ts                    # API client (existing)
│   └── types/
│       └── chat.ts                   # TypeScript types
├── .env.local                         # Environment variables
└── package.json
```

## Development Workflow

### Step 1: Create Types
```bash
# Create types file
touch src/types/chat.ts
```

### Step 2: Create Chat Service
```bash
# Create service file
touch src/services/chatService.ts
```

### Step 3: Create Chat Hook
```bash
# Create hook file
touch src/hooks/useChat.ts
```

### Step 4: Create ChatKit Component
```bash
# Create component directory
mkdir -p src/components/Chat
touch src/components/Chat/ChatKitWrapper.tsx
```

### Step 5: Create Chat Page
```bash
# Create page
mkdir -p src/app/chat
touch src/app/chat/page.tsx
```

## Testing the Integration

### Test 1: Authentication Flow
1. Log out
2. Try to access `/chat`
3. Should redirect to `/login`
4. Log in
5. Should redirect to `/chat`

### Test 2: Send Message
1. Open `/chat`
2. Type: "Hello"
3. Press Enter
4. Should see your message appear
5. Should see loading indicator
6. Should receive AI response

### Test 3: Task Management
1. Send: "Add a task to buy milk"
2. AI should respond confirming task creation
3. Send: "Show my tasks"
4. AI should list your tasks

### Test 4: Conversation Persistence
1. Send a few messages
2. Refresh the page
3. Messages should reload from backend
4. Send a new message
5. Should continue same conversation

## Troubleshooting

### Issue: "Cannot find module '@ai-sdk/react'"
**Solution**: Install the package:
```bash
npm install ai @ai-sdk/react
```

### Issue: "401 Unauthorized" errors
**Solution**: 
1. Check Better Auth is running
2. Verify you're logged in
3. Check session token is being sent in headers
4. Verify backend accepts Better Auth tokens

### Issue: "Network error" or "Failed to fetch"
**Solution**:
1. Verify backend is running on `http://localhost:8000`
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Check CORS settings in backend
4. Verify backend health endpoint works

### Issue: ChatKit not rendering
**Solution**:
1. Check browser console for errors
2. Verify ChatKit package is installed
3. Check component imports are correct
4. Verify environment variables are set

### Issue: Messages not persisting
**Solution**:
1. Check backend database connection
2. Verify backend chat endpoint is working
3. Check browser network tab for API responses
4. Verify `conversation_id` is being returned

## Production Deployment

### 1. Deploy Frontend
Deploy to Vercel, Netlify, or your preferred platform:
```bash
npm run build
# Deploy dist/ or .next/ directory
```

### 2. Configure Domain Allowlist
1. Get your production URL: `https://your-app.vercel.app`
2. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Add your domain (without trailing slash)
4. Get the domain key

### 3. Set Environment Variables
In your hosting platform, set:
- `NEXT_PUBLIC_API_URL=https://your-backend-url.com`
- `NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key`
- `BETTER_AUTH_URL=https://your-app.vercel.app`
- Other Better Auth variables

### 4. Verify Deployment
1. Visit production URL
2. Log in
3. Test chat functionality
4. Verify all features work

## Next Steps

After completing the quickstart:
1. Implement conversation sidebar (Phase 6)
2. Add tool call visualization (Phase 7)
3. Enhance error handling (Phase 8)
4. Add mobile responsiveness (Phase 10)
5. Polish UI/UX (Phase 11)

## Resources

- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [Better Auth Documentation](https://better-auth.com/docs)
- Backend API Documentation: `backend/docs/chat_api.md`

## Support

If you encounter issues:
1. Check browser console for errors
2. Check backend logs
3. Verify all environment variables
4. Test backend endpoints directly with curl/Postman
5. Review the spec.md for detailed requirements
