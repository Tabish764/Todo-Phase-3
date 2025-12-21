from typing import List, Optional
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Task, TaskCreateRequest, TaskUpdateRequest
from uuid import UUID
from datetime import datetime


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_create: TaskCreateRequest) -> Task:
        """Create a new task in the database"""
        try:
            # Create the task instance
            task = Task(
                title=task_create.title,
                description=task_create.description,
                completed=False  # Default to False
            )

            # Add to session and commit
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)

            return task
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Error creating task: {str(e)}")

    async def get_task(self, task_id: UUID) -> Optional[Task]:
        """Get a task by ID from the database"""
        try:
            statement = select(Task).where(Task.id == task_id)
            result = await self.session.execute(statement)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise Exception(f"Error getting task: {str(e)}")

    async def get_all_tasks(self) -> List[Task]:
        """Get all tasks from the database"""
        try:
            statement = select(Task)
            result = await self.session.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise Exception(f"Error getting tasks: {str(e)}")

    async def update_task(self, task_id: UUID, task_update: TaskUpdateRequest) -> Optional[Task]:
        """Update a task in the database"""
        try:
            # Get the existing task
            statement = select(Task).where(Task.id == task_id)
            result = await self.session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return None

            # Update the task fields
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.description is not None:
                task.description = task_update.description
            if task_update.completed is not None:
                task.completed = task_update.completed

            # Update the updated_at timestamp
            task.updated_at = datetime.now()

            # Commit changes
            await self.session.commit()
            await self.session.refresh(task)

            return task
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Error updating task: {str(e)}")

    async def delete_task(self, task_id: UUID) -> bool:
        """Delete a task from the database"""
        try:
            statement = select(Task).where(Task.id == task_id)
            result = await self.session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return False

            await self.session.delete(task)
            await self.session.commit()

            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Error deleting task: {str(e)}")

    async def get_tasks_by_user_id(self, user_id: str) -> List[Task]:
        """Get all tasks for a specific user from the database"""
        try:
            statement = select(Task).where(Task.user_id == user_id)
            result = await self.session.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise Exception(f"Error getting tasks for user: {str(e)}")

    async def create_task_for_user(self, user_id: str, task_create: TaskCreateRequest) -> Task:
        """Create a new task for a specific user in the database"""
        try:
            task = Task(
                user_id=user_id,
                title=task_create.title,
                description=task_create.description,
                completed=False  # Default to False
            )

            # Add to session and commit
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)

            return task
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Error creating task for user: {str(e)}")

    async def update_task_for_user(self, user_id: str, task_id: UUID, task_update: TaskUpdateRequest) -> Optional[Task]:
        """Update a task for a specific user in the database"""
        try:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await self.session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return None

            # Update the task fields
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.description is not None:
                task.description = task_update.description
            if task_update.completed is not None:
                task.completed = task_update.completed

            # Update the updated_at timestamp
            task.updated_at = datetime.now()

            # Commit changes
            await self.session.commit()
            await self.session.refresh(task)

            return task
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Error updating task for user: {str(e)}")

    async def delete_task_for_user(self, user_id: str, task_id: UUID) -> bool:
        """Delete a task for a specific user from the database"""
        try:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await self.session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                return False

            await self.session.delete(task)
            await self.session.commit()

            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Error deleting task for user: {str(e)}")