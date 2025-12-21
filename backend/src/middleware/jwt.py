from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from ..utils.better_auth_session import get_current_user_from_session
import os


def verify_user_access(user_id_from_token: str, user_id_from_path: str) -> bool:
    """
    Verify that the user_id in the session token matches the user_id in the URL path
    This prevents users from accessing other users' resources
    """
    return user_id_from_token == user_id_from_path


def get_current_user(token_data: Dict[str, Any] = Depends(get_current_user_from_session)):
    """
    Dependency to get the current user from the Better Auth session
    """
    return token_data