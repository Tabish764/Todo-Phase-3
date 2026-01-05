"""
MCP Service Base

This module implements the base service layer for MCP tools to interact with the task management system.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Task  # Using correct task model


class BaseMCPService(ABC):
    """Base class for MCP services"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def validate_user_ownership(self, task_id: int, user_id: str) -> bool:
        """Validate that a user owns a specific task"""
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.db_session.execute(stmt)
        task = result.scalar_one_or_none()
        return task is not None


class TaskMCPService(BaseMCPService):
    """Service class for task-related MCP operations"""

    async def create_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None
    ) -> Task:
        """Create a new task for the user"""
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False
        )
        self.db_session.add(task)
        await self.db_session.commit()
        await self.db_session.refresh(task)
        return task

    async def get_user_tasks(
        self,
        user_id: str,
        status_filter: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[List[Task], int]:
        """Get tasks for a user with optional filtering and pagination"""
        # Build query
        stmt = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status_filter:
            if status_filter == "completed":
                stmt = stmt.where(Task.completed == True)
            elif status_filter == "pending":
                stmt = stmt.where(Task.completed == False)
            # If status_filter is "all" or any other value, no additional filter needed

        # Count total
        count_stmt = select(Task).where(Task.user_id == user_id)
        if status_filter:
            if status_filter == "completed":
                count_stmt = count_stmt.where(Task.completed == True)
            elif status_filter == "pending":
                count_stmt = count_stmt.where(Task.completed == False)

        count_result = await self.db_session.execute(count_stmt)
        total_count = len(count_result.scalars().all())

        # Apply sorting and pagination
        stmt = stmt.order_by(Task.created_at.desc()).offset(offset).limit(limit)
        result = await self.db_session.execute(stmt)
        tasks = result.scalars().all()

        return tasks, total_count

    async def update_task_completion(
        self,
        task_id: int,
        user_id: str,
        completed: bool
    ) -> Optional[Task]:
        """Update the completion status of a task"""
        # Verify ownership
        if not await self.validate_user_ownership(task_id, user_id):
            return None

        stmt = select(Task).where(Task.id == task_id)
        result = await self.db_session.execute(stmt)
        task = result.scalar_one_or_none()

        if task:
            task.completed = completed
            task.updated_at = datetime.now()
            await self.db_session.commit()
            await self.db_session.refresh(task)

        return task

    async def update_task_details(
        self,
        task_id: int,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[Task]:
        """Update task details (title and/or description)"""
        # Verify ownership
        if not await self.validate_user_ownership(task_id, user_id):
            return None

        stmt = select(Task).where(Task.id == task_id)
        result = await self.db_session.execute(stmt)
        task = result.scalar_one_or_none()

        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            task.updated_at = datetime.now()
            await self.db_session.commit()
            await self.db_session.refresh(task)

        return task

    async def delete_task(
        self,
        task_id: int,
        user_id: str
    ) -> bool:
        """Delete a task if it belongs to the user"""
        # Verify ownership
        if not await self.validate_user_ownership(task_id, user_id):
            return False

        stmt = select(Task).where(Task.id == task_id)
        result = await self.db_session.execute(stmt)
        task = result.scalar_one_or_none()

        if task:
            await self.db_session.delete(task)
            await self.db_session.commit()
            return True

        return False

    async def get_task_by_id(
        self,
        task_id: int,
        user_id: str
    ) -> Optional[Task]:
        """Get a specific task by ID for a user"""
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()