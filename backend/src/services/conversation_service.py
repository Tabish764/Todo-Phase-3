"""Conversation service for the Todo AI Chatbot application."""
from typing import Optional, List, Tuple
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime

from src.models.conversation import Conversation, ConversationCreate
from src.models.message import Message, MessageCreate, MessageRole
from src.utils.errors import NotFoundError, ForbiddenError


class ConversationService:
    """Service class for managing conversations and messages."""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_conversation(self, user_id: str, title: str, commit: bool = False) -> Conversation:
        """Create a new conversation.
        
        Args:
            user_id: User ID
            title: Conversation title
            commit: If True, commit immediately. If False, use flush (for transactions).
        """
        conversation = Conversation(
            user_id=user_id,
            title=title
        )
        self.session.add(conversation)
        if commit:
            await self.session.commit()
        else:
            await self.session.flush()
        await self.session.refresh(conversation)
        return conversation

    async def get_user_conversations(self, user_id: str, limit: int = 20, offset: int = 0) -> Tuple[List[Conversation], int]:
        """Get all conversations for a user with pagination."""
        # Get total count
        count_statement = select(Conversation).where(Conversation.user_id == user_id)
        count_result = await self.session.exec(count_statement)
        total = len(count_result.all())
        
        # Get paginated results
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).offset(offset).limit(limit)
        
        result = await self.session.exec(statement)
        conversations = result.all()
        
        return conversations, total

    async def get_conversation(self, conversation_id: int, user_id: str) -> Conversation:
        """Get a conversation by ID for a specific user."""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await self.session.exec(statement)
        conversation = result.first()
        
        if not conversation:
            raise NotFoundError(
                message="Conversation not found",
                resource="conversation",
                resource_id=str(conversation_id)
            )
        
        return conversation

    async def get_conversation_by_id(self, conversation_id: int, user_id: str) -> Conversation:
        """Get a conversation by ID for a specific user (alias for get_conversation)."""
        return await self.get_conversation(conversation_id, user_id)

    async def get_conversation_history(self, conversation_id: int, user_id: str) -> List[Message]:
        """Get all messages for a conversation."""
        # First verify the conversation belongs to the user
        await self.get_conversation(conversation_id, user_id)
        
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())
        
        result = await self.session.exec(statement)
        messages = result.all()
        
        return messages

    async def get_messages_for_conversation(self, conversation_id: int, user_id: str, limit: int = 50, offset: int = 0) -> Tuple[List[Message], int]:
        """Get paginated messages for a conversation."""
        # First verify the conversation belongs to the user
        await self.get_conversation(conversation_id, user_id)
        
        # Get total count
        count_statement = select(Message).where(Message.conversation_id == conversation_id)
        count_result = await self.session.exec(count_statement)
        total = len(count_result.all())
        
        # Get paginated results
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).offset(offset).limit(limit)
        
        result = await self.session.exec(statement)
        messages = result.all()
        
        return messages, total

    async def get_conversation_context(self, conversation_id: int, user_id: str, limit: int = 10) -> List[Message]:
        """Get recent messages from a conversation for context."""
        # First verify the conversation belongs to the user
        await self.get_conversation(conversation_id, user_id)
        
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit)
        
        result = await self.session.exec(statement)
        messages = result.all()
        
        # Return in chronological order (oldest to newest for context)
        return list(reversed(messages))

    async def create_message(self, message_data: MessageCreate, commit: bool = False) -> Message:
        """Create a new message in a conversation.
        
        Args:
            message_data: Message data
            commit: If True, commit immediately. If False, use flush (for transactions).
        """
        message = Message(
            conversation_id=message_data.conversation_id,
            user_id=message_data.user_id,
            role=message_data.role,
            content=message_data.content,
            tool_calls=message_data.tool_calls
        )
        self.session.add(message)
        if commit:
            await self.session.commit()
        else:
            await self.session.flush()
        await self.session.refresh(message)
        return message

    async def add_message_to_conversation(self, conversation_id: int, user_id: str, role: str, content: str, tool_calls_data: Optional[dict] = None) -> Message:
        """Add a message to a conversation."""
        # Verify conversation belongs to user
        await self.get_conversation(conversation_id, user_id)
        
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls_data
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def search_messages_in_conversation(self, conversation_id: int, user_id: str, search_term: Optional[str] = None, role: Optional[str] = None, limit: int = 50, offset: int = 0) -> Tuple[List[Message], int]:
        """Search/filter messages in a conversation."""
        # First verify the conversation belongs to the user
        await self.get_conversation(conversation_id, user_id)
        
        # Build query
        statement = select(Message).where(Message.conversation_id == conversation_id)
        
        # Add search filters
        if search_term:
            statement = statement.where(Message.content.contains(search_term))
        
        if role:
            statement = statement.where(Message.role == role)
        
        # Get total count
        count_result = await self.session.exec(statement)
        total = len(count_result.all())
        
        # Get paginated results
        statement = statement.order_by(Message.created_at.asc()).offset(offset).limit(limit)
        result = await self.session.exec(statement)
        messages = result.all()
        
        return messages, total

    async def update_conversation_title(self, conversation_id: int, title: str) -> Conversation:
        """Update the title of a conversation."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        result = await self.session.exec(statement)
        conversation = result.first()
        
        if not conversation:
            raise NotFoundError(
                message="Conversation not found",
                resource="conversation",
                resource_id=str(conversation_id)
            )
        
        conversation.title = title
        conversation.updated_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def update_conversation_timestamp(self, conversation_id: int, commit: bool = False) -> Conversation:
        """Update the updated_at timestamp of a conversation.
        
        Args:
            conversation_id: Conversation ID
            commit: If True, commit immediately. If False, use flush (for transactions).
        """
        statement = select(Conversation).where(Conversation.id == conversation_id)
        result = await self.session.exec(statement)
        conversation = result.first()
        
        if not conversation:
            raise NotFoundError(
                message="Conversation not found",
                resource="conversation",
                resource_id=str(conversation_id)
            )
        
        conversation.updated_at = datetime.now()
        if commit:
            await self.session.commit()
        else:
            await self.session.flush()
        await self.session.refresh(conversation)
        return conversation
