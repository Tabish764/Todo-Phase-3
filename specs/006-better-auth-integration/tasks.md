# Tasks: Better Auth Integration

## Feature Overview
Implement Better Auth authentication with JWT and JWKS verification for Phase 2 of the application. The solution will provide secure user authentication and authorization with stateful sessions managed by Better Auth on the frontend and JWT verification on the backend.

## Implementation Strategy
- MVP: Implement basic signup/login with JWT verification for task access
- Incremental delivery: Start with core auth functionality, then add protections
- Each user story should be independently testable

## Dependencies
- Frontend: Next.js, Better Auth, Drizzle ORM, PostgreSQL
- Backend: FastAPI, PyJWT, Cryptography
- Database: PostgreSQL with Drizzle ORM for user/session management

## Phase 1: Setup Tasks
- [X] T001 Install frontend dependencies: npm install better-auth drizzle-orm postgres
- [X] T002 Install backend dependencies: uv add pyjwt cryptography
- [X] T003 [P] Create frontend environment variables file (frontend/.env.local)
- [X] T004 [P] Create backend environment variables file (backend/.env)
- [X] T005 [P] Create frontend lib directory structure (frontend/lib/)
- [X] T006 [P] Create backend utils directory structure (backend/utils/)

## Phase 2: Foundational Tasks
- [X] T007 Create database schema for users table in frontend/drizzle/schema.ts
- [X] T008 Create database schema for sessions table in frontend/drizzle/schema.ts
- [X] T009 Create database schema for jwks table in frontend/drizzle/schema.ts
- [X] T010 Create database connection in frontend/lib/db-drizzle.ts
- [X] T011 Create Better Auth configuration in frontend/lib/auth.ts
- [X] T012 Create JWT utility functions in backend/utils/auth.py
- [X] T013 Create JWT middleware in backend/middleware/jwt.py
- [X] T014 Configure backend settings in backend/config.py

## Phase 3: [US1] User Registration and Authentication
**Story Goal**: Users can register, login, and logout with email/password

**Independent Test Criteria**:
- User can successfully register with email/password
- User can successfully login with registered credentials
- User can successfully logout and lose access to protected resources

**Tasks**:
- [X] T015 [P] [US1] Create auth API routes handler in frontend/app/api/auth/[...all]/route.ts
- [X] T016 [P] [US1] Create auth client hooks in frontend/lib/auth-client.ts
- [X] T017 [P] [US1] Create signup page component in frontend/app/signup/page.tsx
- [X] T018 [P] [US1] Create login page component in frontend/app/login/page.tsx
- [X] T019 [US1] Create JWKS endpoint in frontend/app/api/jwks/route.ts
- [X] T020 [US1] Update backend task routes with JWT middleware in backend/routes/tasks.py

## Phase 4: [US2] Protected Task Access
**Story Goal**: Users can only access their own tasks through authenticated API calls

**Independent Test Criteria**:
- Authenticated users can access their own tasks
- Unauthenticated users are denied access to tasks (401)
- Users cannot access other users' tasks (403)

**Tasks**:
- [X] T021 [P] [US2] Create API client with JWT support in frontend/lib/api.ts
- [X] T022 [P] [US2] Create protected task route component in frontend/app/tasks/[user_id]/page.tsx
- [X] T023 [US2] Implement JWT token verification in backend/middleware/jwt.py
- [X] T024 [US2] Implement user access verification in backend/middleware/jwt.py
- [X] T025 [US2] Update task route to use auth middleware in backend/routes/tasks.py

## Phase 5: Polish & Cross-Cutting Concerns
- [X] T026 Add error handling to auth pages and API calls
- [X] T027 Add loading states to auth pages
- [X] T028 Add validation to signup/login forms
- [X] T029 Add session management to frontend components
- [X] T030 Add logging to authentication events
- [X] T031 Update README with auth setup instructions
- [X] T032 Test complete auth flow: signup → login → access tasks → logout

## Parallel Execution Examples
- Tasks T015-T018 can run in parallel (different frontend files)
- Tasks T007-T009 can run in parallel (database schema creation)
- Tasks T021-T022 can run in parallel (frontend API and component)

## MVP Scope
The MVP includes US1 (user registration and authentication) which provides the core functionality of the auth system. This includes signup, login, and basic JWT verification.