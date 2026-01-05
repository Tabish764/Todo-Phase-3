from typing import Optional, Dict, Any, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

if TYPE_CHECKING:
    from conversation import Conversation  # ✅ Use src.models

class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"

class MessageBase(SQLModel):
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: str
    role: MessageRole = Field(default=MessageRole.user)
    content: str
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSONB))

class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    
    conversation: "Conversation" = Relationship(back_populates="messages")

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    created_at: datetime
