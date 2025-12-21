from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from uuid import UUID, uuid4


class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime

    @field_validator('title')
    def validate_title(cls, v):
        if not v or len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v

    @classmethod
    def create(cls, title: str, description: Optional[str] = None):
        now = datetime.now()
        return cls(
            id=str(uuid4()),
            title=title,
            description=description,
            completed=False,
            created_at=now,
            updated_at=now
        )

    def update(self, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None):
        now = datetime.now()
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if completed is not None:
            self.completed = completed
        self.updated_at = now
        return self