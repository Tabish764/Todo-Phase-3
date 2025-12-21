import jwt
from jwt import PyJWKClient
from typing import Dict, Any, Optional
import os
from datetime import datetime
import logging
from functools import lru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
# Set up logger for authentication events
logger = logging.getLogger(__name__)

# HTTP Bearer security scheme
security = HTTPBearer()


@lru_cache(maxsize=1)
def get_jwk_client() -> PyJWKClient:
    """
    Get a cached PyJWKClient for JWKS verification.

    The client fetches public keys from Better Auth's JWKS endpoint
    and caches them for efficient verification.
    """
    # Better Auth JWKS endpoint
    jwks_url = f"{os.getenv('BETTER_AUTH_URL', 'http://localhost:3000')}/.well-known/jwks.json"

    return PyJWKClient(jwks_url)


class JWTUtil:
    """
    Utility class for JWT operations including verification using HMAC (HS256)
    """

    def __init__(self, jwks_url: Optional[str] = None):
        """
        Initialize JWTUtil with optional JWKS URL.
        
        Args:
            jwks_url: Optional JWKS endpoint URL (currently not used for HMAC verification)
        """
        self.jwks_url = jwks_url or (
            f"{os.getenv('BETTER_AUTH_URL', 'http://localhost:3000')}/.well-known/jwks.json"
        )
        self._secret = None

    @property
    def secret(self) -> str:
        """
        Get the shared secret for JWT verification.
        Caches the secret to avoid repeated environment variable lookups.
        
        Returns:
            str: The BETTER_AUTH_SECRET from environment
            
        Raises:
            ValueError: If BETTER_AUTH_SECRET is not set
        """
        if self._secret is None:
            self._secret = os.getenv('BETTER_AUTH_SECRET')
            if not self._secret:
                logger.error("BETTER_AUTH_SECRET environment variable is not set")
                raise ValueError("BETTER_AUTH_SECRET environment variable must be set")
        return self._secret

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify JWT token using JWKS and return the payload
        """
        try:
            # Get JWKS client and signing key
            jwk_client = get_jwk_client()
            signing_key = jwk_client.get_signing_key_from_jwt(token)

            # Verify and decode the JWT
            # Better Auth uses EdDSA (Ed25519) or RS256 by default
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["EdDSA", "RS256", "HS256"],  # Adding HS256 as fallback
                options={"verify_aud": False}  # Better Auth doesn't use audience claim
            )

            # Extract user ID for logging
            # Better Auth tokens might have user ID in different locations
            user_id = payload.get('user', {}).get('id') or payload.get('id') or payload.get('sub')
            if not user_id:
                logger.warning(f"Token payload missing user ID: {payload}")
                raise Exception("Token payload missing user ID")

            logger.info(f"Successfully verified token for user: {user_id}")

            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token verification failed: Token has expired")
            raise Exception("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token verification failed: Invalid token - {str(e)}")
            raise Exception(f"Invalid token: {str(e)}")
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            raise Exception(f"Token verification failed: {str(e)}")

    # NOTE: The following methods are kept for potential future use with RSA/JWKS
    # but are not currently used in HMAC-based verification
    
    def get_jwks(self) -> Dict[str, Any]:
        """
        Fetch JWKS from the authentication service.
        Currently not used for HMAC verification but kept for future compatibility.
        
        Returns:
            Dict[str, Any]: JWKS response containing public keys
            
        Raises:
            Exception: If JWKS fetch fails
        """
        try:
            logger.info(f"Fetching JWKS from {self.jwks_url}")
            response = requests.get(self.jwks_url, timeout=5)
            response.raise_for_status()
            jwks = response.json()
            logger.info(f"Successfully fetched JWKS with {len(jwks.get('keys', []))} keys")
            return jwks
        except requests.RequestException as e:
            logger.error(f"Error fetching JWKS from {self.jwks_url}: {e}")
            raise Exception(f"Failed to fetch JWKS: {str(e)}")

    def get_key_from_kid(self, kid: str, jwks: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find the key in JWKS that matches the given kid (Key ID).
        Currently not used for HMAC verification but kept for future compatibility.
        
        Args:
            kid: Key ID to search for
            jwks: JWKS dictionary containing keys
            
        Returns:
            Dict[str, Any]: Matching key from JWKS
            
        Raises:
            Exception: If key with given kid is not found
        """
        for key in jwks.get('keys', []):
            if key.get('kid') == kid:
                logger.info(f"Found matching key with kid: {kid}")
                return key
        
        logger.warning(f"Key with kid '{kid}' not found in JWKS")
        raise Exception(f"Key with kid '{kid}' not found in JWKS")


# ============================================================================
# FASTAPI DEPENDENCIES
# ============================================================================

@lru_cache()
def get_jwt_util() -> JWTUtil:
    """
    Factory function to get cached JWTUtil instance.
    Uses lru_cache to ensure single instance across requests.
    
    Returns:
        JWTUtil: Cached JWT utility instance
    """
    return JWTUtil()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_util: JWTUtil = Depends(get_jwt_util)
) -> Dict[str, Any]:
    """
    FastAPI dependency to extract and verify the current user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials from request header
        jwt_util: JWT utility instance for token verification
        
    Returns:
        Dict[str, Any]: Decoded token payload containing user information
        
    Raises:
        HTTPException: 401 if token is invalid or verification fails
    """
    token = credentials.credentials
    
    try:
        payload = jwt_util.verify_token(token)
        
        # Validate that payload contains user information
        if "user" not in payload or "id" not in payload.get("user", {}):
            logger.warning("Token payload missing required user information")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: Missing user information",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
        
    except Exception as e:
        # Log the error and raise HTTP 401
        logger.warning(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


# ============================================================================
# OPTIONAL: Additional utility functions
# ============================================================================

def extract_user_id(token_payload: Dict[str, Any]) -> Optional[str]:
    """
    Safely extract user ID from token payload.
    
    Args:
        token_payload: Decoded JWT payload
        
    Returns:
        Optional[str]: User ID if present, None otherwise
    """
    return token_payload.get("user", {}).get("id")


def extract_user_email(token_payload: Dict[str, Any]) -> Optional[str]:
    """
    Safely extract user email from token payload.
    
    Args:
        token_payload: Decoded JWT payload
        
    Returns:
        Optional[str]: User email if present, None otherwise
    """
    return token_payload.get("user", {}).get("email")