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

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.
- [Better Auth Documentation](https://better-auth.com/docs) - for authentication features

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
