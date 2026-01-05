This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

## Authentication Setup

This project includes Better Auth integration with JWT and JWKS verification. Follow these steps to set up authentication:

### Prerequisites
- PostgreSQL database running
- Backend API server running on http://localhost:8000

### Environment Variables
Create a `.env.local` file in the root directory with the following content:

```
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
BETTER_AUTH_SECRET=your-32-char-secret-here-make-it-secure
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Features
- User registration and login with email/password
- JWT token-based authentication
- Protected routes for user-specific tasks
- Session management via Better Auth

### Available Pages
- `/signup` - User registration
- `/login` - User login
- `/tasks/[user_id]` - User-specific task management
- `/chat` - AI chat interface

### ChatKit Setup and Configuration

This project uses OpenAI ChatKit via the `@ai-sdk/react` library for the chat interface. Here's how to set it up:

#### Installation
The following packages are already installed:
- `@ai-sdk/react` - Provides the ChatKit components and hooks
- `ai` - AI SDK utilities

#### Environment Variables
Add the following to your `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here  # Optional for localhost
```

#### Chat Features
- Real-time chat interface with user and assistant messages
- Tool call visualization for AI tool usage
- Conversation persistence with history
- Loading indicators during AI processing
- Error handling with retry functionality
- Mobile-responsive design

### Domain Allowlist Setup (Production)

For production deployment with OpenAI ChatKit, you need to configure domain allowlisting:

1. Deploy frontend to production (Vercel, etc.)
2. Get production URL: `https://your-app.vercel.app`
3. Add domain to OpenAI: https://platform.openai.com/settings/organization/security/domain-allowlist
4. Obtain domain key
5. Set `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` in production environment

**Note**: Localhost works without domain allowlist during development.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.
- [Better Auth Documentation](https://better-auth.com/docs) - for authentication features

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
