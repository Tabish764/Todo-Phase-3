Implement Better Auth authentication with JWT and JWKS verification.

## Context
Phase 2 requires user authentication. Use Better Auth on Next.js frontend with JWT plugin, and verify tokens on FastAPI backend using JWKS (JSON Web Key Set) for stateless authentication.

## Architecture Overview

Frontend (Better Auth) → Issues JWT tokens → Backend verifies using JWKS public keys

Flow:
1. User signs in → Better Auth generates JWT (signed with private key)
2. Frontend sends JWT in Authorization header
3. Backend fetches public keys from JWKS endpoint
4. Backend verifies JWT signature using public key
5. Backend extracts user_id and filters data

## Frontend Requirements

### 1. Install Dependencies
```bash
cd frontend
npm install better-auth drizzle-orm postgres
```

### 2. Better Auth Configuration
File: `frontend/lib/auth.ts`
```typescript
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "./db-drizzle";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
  }),
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    // JWT plugin generates tokens with EdDSA/RS256
  ],
});
```

### 3. Database Setup (Drizzle)
File: `frontend/lib/db-drizzle.ts`
```typescript
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

const client = postgres(process.env.DATABASE_URL!);
export const db = drizzle(client);
```

File: `frontend/drizzle/schema.ts`
```typescript
import { pgTable, text, timestamp } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  emailVerified: timestamp("emailVerified"),
  name: text("name"),
  createdAt: timestamp("createdAt").notNull(),
  updatedAt: timestamp("updatedAt").notNull(),
});

export const sessions = pgTable("sessions", {
  id: text("id").primaryKey(),
  userId: text("userId").notNull().references(() => users.id),
  expiresAt: timestamp("expiresAt").notNull(),
  token: text("token").notNull(),
  createdAt: timestamp("createdAt").notNull(),
  updatedAt: timestamp("updatedAt").notNull(),
});

export const jwks = pgTable("jwks", {
  id: text("id").primaryKey(),
  publicKey: text("publicKey").notNull(),
  privateKey: text("privateKey").notNull(),
  createdAt: timestamp("createdAt").notNull(),
});
```

### 4. JWKS Endpoint
File: `frontend/app/api/jwks/route.ts` or `frontend/app/.well-known/jwks.json/route.ts`
```typescript
import { db } from "@/lib/db-drizzle";
import { jwks } from "@/drizzle/schema";

export async function GET() {
  const keys = await db.select().from(jwks);
  
  const jwksResponse = {
    keys: keys.map((key) => {
      const publicKey = JSON.parse(key.publicKey);
      return {
        ...publicKey,
        kid: key.id,
      };
    }),
  };
  
  return new Response(JSON.stringify(jwksResponse), {
    status: 200,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
```

### 5. Auth API Routes
File: `frontend/app/api/auth/[...all]/route.ts`
```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

### 6. Auth Client Hook
File: `frontend/lib/auth-client.ts`
```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

export const { useSession, signIn, signUp, signOut } = authClient;
```

### 7. Auth Pages

**Signup Page**: `frontend/app/signup/page.tsx`
```typescript
"use client";
import { useState } from "react";
import { signUp } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const result = await signUp.email({
        email,
        password,
        name: email.split("@")[0],
      });
      if (result.data) {
        router.push(`/tasks/${result.data.user.id}`);
      }
    } catch (err) {
      setError("Signup failed");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form UI with email, password inputs */}
    </form>
  );
}
```

**Login Page**: `frontend/app/login/page.tsx`
```typescript
"use client";
import { useState } from "react";
import { signIn } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = await signIn.email({ email, password });
    if (result.data) {
      router.push(`/tasks/${result.data.user.id}`);
    }
  };

  return <form onSubmit={handleSubmit}>{/* Form UI */}</form>;
}
```

### 8. Protect Task Routes
File: `frontend/app/tasks/[user_id]/page.tsx`
```typescript
"use client";
import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function TasksPage({ params }: { params: { user_id: string } }) {
  const { data: session, isPending } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/login");
    }
  }, [session, isPending, router]);

  if (isPending) return <div>Loading...</div>;
  if (!session) return null;

  return <div>{/* Task list UI */}</div>;
}
```

### 9. API Client with JWT
File: `frontend/lib/api.ts`
```typescript
import { authClient } from "./auth-client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAuthHeaders() {
  const session = await authClient.getSession();
  if (!session?.data) throw new Error("Not authenticated");
  
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${session.data.session.token}`,
  };
}

export const api = {
  async getTasks(userId: string) {
    const headers = await getAuthHeaders();
    const res = await fetch(`${API_URL}/api/${userId}/tasks`, { headers });
    return res.json();
  },
  // ... other methods
};
```

## Backend Requirements

### 1. Install Dependencies
```bash
cd backend
uv add pyjwt cryptography
```

### 2. Configuration
File: `backend/config.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    better_auth_url: str = "http://localhost:3000"
    better_auth_secret: str
    cors_origins: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 3. JWKS Client
File: `backend/utils/auth.py`
```python
from jwt import PyJWKClient
import jwt
from functools import lru_cache
from typing import Dict
from config import settings

@lru_cache(maxsize=1)
def get_jwk_client() -> PyJWKClient:
    """Get cached JWKS client."""
    jwks_url = f"{settings.better_auth_url}/.well-known/jwks.json"
    return PyJWKClient(jwks_url)

def verify_jwt_token(token: str) -> Dict[str, str]:
    """Verify JWT and extract user info."""
    try:
        jwk_client = get_jwk_client()
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["EdDSA", "RS256"],
            options={"verify_aud": False}
        )
        
        user_id = payload.get("sub") or payload.get("user_id")
        email = payload.get("email", "")
        
        if not user_id:
            raise ValueError("Missing user_id in token")
        
        return {"user_id": user_id, "email": email}
        
    except jwt.exceptions.PyJWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")
```

### 4. JWT Middleware
File: `backend/middleware/jwt.py`
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.auth import verify_jwt_token as verify_token
from typing import Dict

security = HTTPBearer()

def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, str]:
    """Verify JWT from Authorization header."""
    try:
        return verify_token(credentials.credentials)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": str(e)},
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_user_access(
    user_id: str,
    current_user: Dict[str, str] = Depends(verify_jwt_token)
) -> Dict[str, str]:
    """Verify user_id matches JWT token."""
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID mismatch"
        )
    return current_user
```

### 5. Update Task Routes
File: `backend/routes/tasks.py`
```python
from middleware.jwt import verify_user_access

@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    current_user: Dict = Depends(verify_user_access),
    db: Session = Depends(get_session),
):
    """Get tasks (JWT verified, user isolated)."""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = db.exec(statement).all()
    return {"success": True, "data": tasks}
```

## Environment Variables

**Frontend `.env.local`:**
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-32-char-secret
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000

**Backend `.env`:**
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-32-char-secret
BETTER_AUTH_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000

## Success Criteria
- ✅ User can signup with email/password
- ✅ User can login
- ✅ JWT token issued on login
- ✅ JWKS endpoint returns public keys
- ✅ Backend verifies JWT using JWKS
- ✅ Protected routes redirect to login
- ✅ Users only see their own tasks
- ✅ 401 for invalid/missing token
- ✅ 403 for user_id mismatch

## Testing Steps
1. Run frontend: `cd frontend && npm run dev`
2. Run backend: `cd backend && uvicorn main:app --reload`
3. Visit JWKS: http://localhost:3000/.well-known/jwks.json
4. Signup at /signup
5. Login at /login
6. Access /tasks/{user_id} (should work)
7. Try /tasks/{other_user_id} (should fail with 403)