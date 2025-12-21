import os
import logging
from typing import Dict, Any, Optional
from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..database.session import get_db_session
from ..database.models import User, Session

logger = logging.getLogger(__name__)

class BetterAuthSessionUtil:
    """
    Utility class for Better Auth session-based authentication
    """

    def __init__(self):
        pass

    async def verify_session_token(self, token: str, db: AsyncSession) -> Dict[str, Any]:
        """
        Verify session token against the database and return user information
        """
        try:
            # Use raw SQL to query the sessions table with correct column names
            # This avoids potential issues with SQLAlchemy field-to-column mapping
            from sqlalchemy import text

            # Query the sessions table for the given token using actual DB column names
            session_sql = text("""
                SELECT id, "userId", "expiresAt", token, "ipAddress", "userAgent", "createdAt", "updatedAt"
                FROM sessions
                WHERE token = :token
            """)
            session_result = await db.execute(session_sql, {"token": token})
            session_row = session_result.first()

            if not session_row:
                logger.warning(f"Invalid session token: {token}")
                raise Exception("Invalid session token")

            # Extract session data from the row
            session_record = {
                'id': session_row[0],
                'user_id': session_row[1],  # userId
                'expires_at': session_row[2],  # expiresAt
                'token': session_row[3],
                'ip_address': session_row[4],  # ipAddress
                'user_agent': session_row[5],  # userAgent
                'created_at': session_row[6],  # createdAt
                'updated_at': session_row[7]   # updatedAt
            }

            # Check if the session has expired
            from datetime import datetime
            if session_record['expires_at'].replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
                logger.warning(f"Session token has expired: {token}")
                raise Exception("Session token has expired")

            # Query the user associated with this session using actual DB column names
            user_sql = text("""
                SELECT id, email, "emailVerified", name, image, password, "createdAt", "updatedAt"
                FROM users
                WHERE id = :user_id
            """)
            user_result = await db.execute(user_sql, {"user_id": session_record['user_id']})
            user_row = user_result.first()

            if not user_row:
                logger.warning(f"Session token {token} has invalid user_id: {session_record['user_id']}")
                raise Exception("Invalid user in session")

            # Extract user data from the row
            user_record = {
                'id': user_row[0],
                'email': user_row[1],
                'name': user_row[3]  # name is at index 3
            }

            # Create a payload similar to what JWT would provide
            payload = {
                "user": {
                    "id": user_record['id'],
                    "email": user_record['email'],
                    "name": user_record['name'],
                },
                "session_id": session_record['id'],
                "expires_at": session_record['expires_at'].isoformat()
            }

            logger.info(f"Successfully verified session token for user: {user_record['id']}")
            return payload

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Session verification failed: {str(e)}")
            raise Exception(f"Session verification failed: {str(e)}")


async def get_current_user_from_session(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    FastAPI dependency to extract and verify the current user from Better Auth session cookie.
    Looks for the session token in cookies (typically named 'better-auth.session-token').
    """
    session_util = BetterAuthSessionUtil()

    # Try to get the session token from cookies
    # Better Auth typically uses cookies with names like 'better-auth.session' or 'authjs.session-token'
    session_token = None

    # Check for common Better Auth cookie names
    # Better Auth typically names its session cookie as 'better-auth.session'
    # but it can vary depending on configuration
    for cookie_name in [
        # Common Better Auth / NextAuth-style cookie names
        "better-auth.session",
        "better-auth.session-token",
        "authjs.session-token",
        "next-auth.session-token",
        # Extra fallbacks if configuration changes
        "session-token",
        "session",
    ]:
        value = request.cookies.get(cookie_name)
        if value:
            session_token = value
            logger.info(f"Found session token in cookie: {cookie_name}")
            break

    # If not found in cookies, also check for it in Authorization header as Bearer token
    # This allows the frontend to send the Better Auth session token directly
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header[7:]  # Remove "Bearer " prefix
            logger.info("Found session token in Authorization Bearer header")
        else:
            logger.debug(
                "No Authorization Bearer header present or it does not start with 'Bearer '"
            )

    if not session_token:
        logger.warning("No session token found in cookies or Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No session token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = await session_util.verify_session_token(session_token, db)

        # Validate that payload contains user information
        if "user" not in payload or "id" not in payload.get("user", {}):
            logger.warning("Session payload missing required user information")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session: Missing user information",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except Exception as e:
        # Log the error and raise HTTP 401
        logger.warning(f"Session authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )