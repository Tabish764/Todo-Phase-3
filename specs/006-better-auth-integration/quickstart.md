# Quickstart Guide: Better Auth Integration

## Overview
This guide provides step-by-step instructions to set up and run the Better Auth integration with JWT and JWKS verification for the frontend and backend applications.

## Prerequisites
- Node.js 18+ installed
- Python 3.9+ installed
- PostgreSQL database running
- Git for version control

## Setup Instructions

### 1. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install better-auth drizzle-orm postgres
```

#### Configure Environment Variables
Create a `.env.local` file in the frontend directory with the following content:
```
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
BETTER_AUTH_SECRET=your-32-char-secret-here-make-it-secure
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Run Database Migrations
```bash
npx drizzle-kit push
```

#### Start the Frontend Application
```bash
npm run dev
```
The frontend will be available at http://localhost:3000

### 2. Backend Setup

#### Install Dependencies
```bash
cd backend
uv add pyjwt cryptography
```

#### Configure Environment Variables
Create a `.env` file in the backend directory with the following content:
```
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
BETTER_AUTH_SECRET=your-32-char-secret-here-make-it-secure
BETTER_AUTH_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000
```

#### Start the Backend Application
```bash
uvicorn main:app --reload
```
The backend will be available at http://localhost:8000

## Verification Steps

### 1. Verify JWKS Endpoint
Visit: http://localhost:3000/.well-known/jwks.json
- Should return a JSON object with public keys
- Verify the response includes the `keys` array

### 2. User Registration
1. Navigate to http://localhost:3000/signup
2. Fill in the registration form with your email and password
3. Submit the form
4. Verify you're redirected to the tasks page

### 3. User Login
1. Navigate to http://localhost:3000/login
2. Enter your registered email and password
3. Submit the form
4. Verify you're redirected to the tasks page

### 4. Task Access Test
1. After logging in, navigate to http://localhost:3000/tasks/{your_user_id}
2. Verify you can see your tasks
3. Try accessing http://localhost:3000/tasks/{different_user_id} (if it exists)
4. Verify you receive a 403 Forbidden error

### 5. API Testing
Test the API endpoints directly:
```bash
# Get tasks for your user (with valid JWT token)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/your_user_id/tasks

# Try to access another user's tasks (should return 403)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/other_user_id/tasks
```

## Troubleshooting

### Common Issues
- **Database Connection**: Ensure PostgreSQL is running and credentials are correct
- **JWT Verification**: Verify that the frontend and backend share the same `BETTER_AUTH_SECRET`
- **CORS Errors**: Check that `CORS_ORIGINS` includes your frontend URL
- **Session Not Persisting**: Ensure cookies are enabled in your browser

### Debugging Tips
- Check browser console for frontend errors
- Check terminal output for both frontend and backend applications
- Verify environment variables are correctly set
- Confirm the JWKS endpoint is accessible and returning keys

## Next Steps
- Implement additional auth pages (password reset, email verification)
- Add more comprehensive error handling
- Set up monitoring and logging for auth events
- Add rate limiting to auth endpoints