# Implementation Plan: Better Auth Integration

## 1. Technical Context

This plan outlines the implementation of Better Auth authentication with JWT and JWKS verification for Phase 2 of the application. The solution will provide secure user authentication and authorization with stateful sessions managed by Better Auth on the frontend and JWT verification on the backend.

### Architecture Overview
- Frontend: Next.js application with Better Auth for user management and JWT generation
- Backend: FastAPI application with JWT verification using JWKS public keys
- Database: PostgreSQL with Drizzle ORM for user and session management

### Key Technologies
- Better Auth: Frontend authentication library
- Next.js: Frontend framework
- FastAPI: Backend framework
- PostgreSQL: Database
- Drizzle ORM: Database ORM
- JWT: Token-based authentication
- JWKS: JSON Web Key Set for key management

## 2. Constitution Check

### Core Principles Alignment
- ✅ Security First: Implements industry-standard JWT and JWKS for secure authentication
- ✅ Test-First: All authentication flows will be covered with unit and integration tests
- ✅ Observability: Authentication events will be logged for monitoring
- ✅ Simplicity: Uses established libraries (Better Auth) rather than custom implementation

## 3. Phase 0: Research & Analysis

### 3.1 JWT Algorithm Selection
**Decision**: RS256 (RSA Signature with SHA-256)
**Rationale**: RS256 is widely supported, well-established, and provides good security for token verification. It's compatible with most JWT libraries and enterprise environments.
**Alternatives considered**:
- EdDSA: More modern and efficient but less widely supported
- HS256: Symmetric algorithm requiring shared secrets (not suitable for our architecture)

### 3.2 Authentication Architecture
**Decision**: Centralized JWKS endpoint on frontend with stateful sessions
**Rationale**: Better Auth provides built-in session management and JWKS endpoint, reducing complexity and maintenance overhead. The stateful approach provides better security with session invalidation capabilities.

### 3.3 User Isolation Strategy
**Decision**: Verify user_id from JWT token matches the user_id in URL path parameters
**Rationale**: Provides an additional layer of security to ensure users can only access their own data, preventing unauthorized access to other users' resources.

## 4. Phase 1: Data Model Design

### 4.1 Database Schema
The following tables will be created using Drizzle ORM in the frontend application:

```typescript
// Users table
export const users = pgTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  emailVerified: timestamp("emailVerified"),
  name: text("name"),
  createdAt: timestamp("createdAt").notNull(),
  updatedAt: timestamp("updatedAt").notNull(),
});

// Sessions table
export const sessions = pgTable("sessions", {
  id: text("id").primaryKey(),
  userId: text("userId").notNull().references(() => users.id),
  expiresAt: timestamp("expiresAt").notNull(),
  token: text("token").notNull(),
  createdAt: timestamp("createdAt").notNull(),
  updatedAt: timestamp("updatedAt").notNull(),
});

// JWKS table
export const jwks = pgTable("jwks", {
  id: text("id").primaryKey(),
  publicKey: text("publicKey").notNull(),
  privateKey: text("privateKey").notNull(),
  createdAt: timestamp("createdAt").notNull(),
});
```

### 4.2 Session Management
- Better Auth will handle session creation and management
- Sessions will be stored in the database with expiration timestamps
- JWT tokens will be issued for API access
- Session invalidation will be handled by Better Auth

## 5. Phase 1: API Contracts

### 5.1 Frontend Auth Endpoints
- `POST /api/auth/signin` - User login
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signout` - User logout
- `GET /api/auth/session` - Get current session
- `GET /.well-known/jwks.json` - JWKS public keys

### 5.2 Backend API Endpoints
- `GET /api/{user_id}/tasks` - Get tasks for specific user (JWT protected)
- `POST /api/{user_id}/tasks` - Create task for specific user (JWT protected)
- `PUT /api/{user_id}/tasks/{task_id}` - Update task (JWT protected)
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task (JWT protected)

### 5.3 Authentication Flow
1. User registers/logs in via frontend
2. Better Auth creates session and returns JWT
3. Frontend stores JWT in memory/cookies
4. Frontend includes JWT in Authorization header for API requests
5. Backend verifies JWT using JWKS endpoint
6. Backend validates user_id in token matches URL parameter
7. Backend processes request if authentication/authorization passes

## 6. Phase 1: Implementation Steps

### 6.1 Frontend Implementation
1. Install dependencies: `npm install better-auth drizzle-orm postgres`
2. Configure Better Auth with database adapter
3. Set up database schema with Drizzle
4. Create JWKS endpoint
5. Implement auth API routes
6. Create auth client hooks
7. Build signup/login pages
8. Protect task routes
9. Create API client with JWT support

### 6.2 Backend Implementation
1. Install dependencies: `uv add pyjwt cryptography`
2. Configure settings with auth URLs and secrets
3. Create JWKS client utility
4. Implement JWT middleware
5. Update task routes with auth protection
6. Add environment variable configuration

### 6.3 Security Considerations
- JWT tokens will be verified using JWKS to prevent key compromise
- User ID in token will be validated against URL parameters
- Session management will be handled by Better Auth
- CORS will be properly configured
- Rate limiting should be considered for auth endpoints

## 7. Phase 1: Quickstart Guide

### 7.1 Prerequisites
- Node.js 18+ for frontend
- Python 3.9+ for backend
- PostgreSQL database
- Environment variables configured

### 7.2 Setup Steps

#### Frontend Setup:
1. Install dependencies:
   ```bash
   cd frontend
   npm install better-auth drizzle-orm postgres
   ```

2. Configure environment variables in `.env.local`:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   BETTER_AUTH_SECRET=your-32-char-secret
   BETTER_AUTH_URL=http://localhost:3000
   NEXT_PUBLIC_APP_URL=http://localhost:3000
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. Run database migrations:
   ```bash
   npx drizzle-kit push
   ```

4. Start the frontend:
   ```bash
   npm run dev
   ```

#### Backend Setup:
1. Install dependencies:
   ```bash
   cd backend
   uv add pyjwt cryptography
   ```

2. Configure environment variables in `.env`:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   BETTER_AUTH_SECRET=your-32-char-secret
   BETTER_AUTH_URL=http://localhost:3000
   CORS_ORIGINS=http://localhost:3000
   ```

3. Start the backend:
   ```bash
   uvicorn main:app --reload
   ```

### 7.3 Testing the Implementation
1. Visit JWKS endpoint: http://localhost:3000/.well-known/jwks.json
2. Register a new user at /signup
3. Login at /login
4. Access tasks at /tasks/{user_id}
5. Verify that accessing other users' tasks returns 403

## 8. Success Criteria
- ✅ User can signup with email/password
- ✅ User can login
- ✅ JWT token issued on login
- ✅ JWKS endpoint returns public keys
- ✅ Backend verifies JWT using JWKS
- ✅ Protected routes redirect to login
- ✅ Users only see their own tasks
- ✅ 401 for invalid/missing token
- ✅ 403 for user_id mismatch

## 9. Risk Analysis & Mitigation
- **Token Security**: Using JWKS prevents hardcoding public keys and allows key rotation
- **Session Management**: Leveraging Better Auth's built-in session management reduces security risks
- **User Isolation**: Verifying user_id in token against URL parameter prevents unauthorized access
- **Database Security**: Using parameterized queries and ORM prevents SQL injection

## 10. Monitoring & Observability
- Log authentication events (login, logout, token verification)
- Monitor failed authentication attempts
- Track token verification performance
- Alert on unusual authentication patterns