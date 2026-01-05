from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.services.conversation_service import ConversationService
from src.models.conversation import Conversation
from src.models.message import Message
from src.database.session import get_db_session
from src.utils.better_auth_session import get_current_user_from_session  # Adjust import based on your auth system
import logging

# Rate limiting imports
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize router
router = APIRouter(prefix="", tags=["conversations"])

# Add rate limit exceeded handler to the router
router._rate_limit_exceeded_handler = _rate_limit_exceeded_handler


@router.post("/{user_id}/conversations", response_model=Conversation, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # Limit to 5 conversation creations per minute per IP
async def create_conversation(
    request: Request,
    user_id: str,
    conversation_data: dict,
    current_user: dict = Depends(get_current_user_from_session),
    db: AsyncSession = Depends(get_db_session)
):
    """Create a new conversation for the authenticated user"""
    current_user_id = current_user.get("user", {}).get("id") or current_user.get("id") or current_user.get("user_id")
    if not current_user_id:
        logger.warning(f"Unauthorized attempt to create conversation: {current_user}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Verify the user_id in the path matches the authenticated user
    if current_user_id != user_id:
        logger.warning(f"User {current_user_id} attempted to create conversation for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot create conversation for another user"
        )

    title = conversation_data.get("title")
    logger.info(f"Creating conversation for user {user_id} with title: {title}")

    service = ConversationService(db)
    try:
        conversation = await service.create_conversation(user_id=user_id, title=title, commit=False)
        await db.commit()  # Commit for standalone operation
        logger.info(f"Successfully created conversation {conversation.id} for user {user_id}")
        return conversation
    except Exception as e:
        logger.error(f"Error creating conversation for user {user_id}: {str(e)}")
        raise


@router.get("/{user_id}/conversations", response_model=dict)
@limiter.limit("30/minute")  # Limit to 30 conversation list requests per minute per IP
async def get_user_conversations(
    request: Request,
    user_id: str,
    current_user: dict = Depends(get_current_user_from_session),
    db: AsyncSession = Depends(get_db_session),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all conversations for the authenticated user, sorted by most recent activity"""
    current_user_id = current_user.get("user", {}).get("id") or current_user.get("id") or current_user.get("user_id")
    if not current_user_id:
        logger.warning(f"Unauthorized attempt to get conversations: {current_user}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Verify the user_id in the path matches the authenticated user
    if current_user_id != user_id:
        logger.warning(f"User {current_user_id} attempted to access conversations for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access another user's conversations"
        )

    logger.info(f"Getting conversations for user {user_id} with limit={limit}, offset={offset}")

    service = ConversationService(db)
    try:
        conversations, total = await service.get_user_conversations(user_id=user_id, limit=limit, offset=offset)
        logger.info(f"Retrieved {len(conversations)} conversations out of {total} total for user {user_id}")

        return {
            "conversations": conversations,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error getting conversations for user {user_id}: {str(e)}")
        raise


@router.get("/{user_id}/conversations/{conversation_id}", response_model=Conversation)
@limiter.limit("60/minute")  # Limit to 60 conversation detail requests per minute per IP
async def get_conversation(
    request: Request,
    user_id: str,
    conversation_id: int,
    current_user: dict = Depends(get_current_user_from_session),
    db: AsyncSession = Depends(get_db_session)
):
    """Get details of a specific conversation"""
    current_user_id = current_user.get("user", {}).get("id") or current_user.get("id") or current_user.get("user_id")
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Verify the user_id in the path matches the authenticated user
    if current_user_id != user_id:
        logger.warning(f"User {current_user_id} attempted to access conversation {conversation_id} for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access another user's conversation"
        )

    service = ConversationService(db)
    conversation = await service.get_conversation_by_id(conversation_id=conversation_id, user_id=user_id)

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or does not belong to user"
        )

    return conversation


@router.post("/{user_id}/conversations/{conversation_id}/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")  # Limit to 20 message additions per minute per IP
async def add_message_to_conversation(
    request: Request,
    user_id: str,
    conversation_id: int,
    message_data: dict,
    current_user: dict = Depends(get_current_user_from_session),
    db: AsyncSession = Depends(get_db_session)
):
    """Add a message to an existing conversation"""
    current_user_id = current_user.get("user", {}).get("id") or current_user.get("id") or current_user.get("user_id")
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Verify the user_id in the path matches the authenticated user
    if current_user_id != user_id:
        logger.warning(f"User {current_user_id} attempted to add message to conversation {conversation_id} for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot add message to another user's conversation"
        )

    role = message_data.get("role")
    content = message_data.get("content")
    tool_calls = message_data.get("tool_calls")

    # Validate required fields
    if not content:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Content is required"
        )

    if role not in ["user", "assistant", "system"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Role must be one of: user, assistant, system"
        )

    service = ConversationService(db)

    try:
        message = await service.add_message_to_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls_data=tool_calls
        )
        return message
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{user_id}/conversations/{conversation_id}/messages", response_model=dict)
@limiter.limit("30/minute")  # Limit to 30 message list requests per minute per IP
async def get_conversation_messages(
    request: Request,
    user_id: str,
    conversation_id: int,
    current_user: dict = Depends(get_current_user_from_session),
    db: AsyncSession = Depends(get_db_session),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """Get all messages in a specific conversation, sorted chronologically"""
    current_user_id = current_user.get("user", {}).get("id") or current_user.get("id") or current_user.get("user_id")
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Verify the user_id in the path matches the authenticated user
    if current_user_id != user_id:
        logger.warning(f"User {current_user_id} attempted to access messages for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access another user's messages"
        )

    service = ConversationService(db)

    try:
        messages, total = await service.get_messages_for_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
            limit=limit,
            offset=offset
        )

        return {
            "messages": messages,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{user_id}/conversations/{conversation_id}/context", response_model=List[Message])
@limiter.limit("30/minute")  # Limit to 30 context requests per minute per IP
async def get_conversation_context(
    request: Request,
    user_id: str,
    conversation_id: int,
    current_user: dict = Depends(get_current_user_from_session),
    db: AsyncSession = Depends(get_db_session),
    limit: int = Query(10, ge=1, le=50)
):
    """Get recent messages from a conversation for context (most recent first)"""
    current_user_id = current_user.get("user", {}).get("id") or current_user.get("id") or current_user.get("user_id")
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Verify the user_id in the path matches the authenticated user
    if current_user_id != user_id:
        logger.warning(f"User {current_user_id} attempted to access context for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access another user's conversation context"
        )

    service = ConversationService(db)

    try:
        messages = await service.get_conversation_context(
            conversation_id=conversation_id,
            user_id=user_id,
            limit=limit
        )

        return messages
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{user_id}/conversations/{conversation_id}/messages/search", response_model=dict)
@limiter.limit("15/minute")  # Limit to 15 search requests per minute per IP
async def search_messages_in_conversation(
    request: Request,
    user_id: str,
    conversation_id: int,
    current_user: dict = Depends(get_current_user_from_session),
    db: AsyncSession = Depends(get_db_session),
    search_term: Optional[str] = Query(None, min_length=1, max_length=100),
    role: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """Search/filter messages in a conversation based on criteria"""
    current_user_id = current_user.get("user", {}).get("id") or current_user.get("id") or current_user.get("user_id")
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Verify the user_id in the path matches the authenticated user
    if current_user_id != user_id:
        logger.warning(f"User {current_user_id} attempted to search messages for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot search another user's messages"
        )

    # Validate role parameter
    if role and role not in ["user", "assistant", "system"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Role must be one of: user, assistant, system"
        )

    service = ConversationService(db)

    try:
        messages, total = await service.search_messages_in_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
            search_term=search_term,
            role=role,
            limit=limit,
            offset=offset
        )

        return {
            "messages": messages,
            "total": total,
            "limit": limit,
            "offset": offset,
            "search_term": search_term,
            "role": role
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
