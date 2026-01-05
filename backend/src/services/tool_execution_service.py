"""Tool Execution Service for the Todo AI Chatbot application."""
from typing import Dict, Any, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from datetime import datetime
import uuid

from src.database.models import Task
from src.utils.logging import app_logger

class ToolExecutionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Routes tool calls and handles session cleanup to prevent Greenlet errors."""
        try:
            if tool_name == "add_task":
                return await self._execute_add_task(arguments)
            elif tool_name == "list_tasks":
                return await self._execute_list_tasks(arguments)
            elif tool_name == "complete_task":
                return await self._execute_complete_task(arguments)
            elif tool_name == "delete_task":
                return await self._execute_delete_task(arguments)
            elif tool_name == "update_task":
                return await self._execute_update_task(arguments)
            else:
                return {"status": "error", "error": f"Tool '{tool_name}' not found"}
        except Exception as e:
            app_logger.error(f"Tool Error ({tool_name}): {str(e)}")
            # This is the most important line to prevent the crash on the 2nd call:
            await self.session.rollback() 
            return {"status": "error", "error": str(e)}

    async def _execute_add_task(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        user_id = arguments.get("user_id")
        task = Task(
            user_id=user_id, 
            title=arguments.get("title"), 
            description=arguments.get("description", ""),
            completed=False
        )
        self.session.add(task)
        # Use flush instead of commit - let the router handle the final commit
        await self.session.flush()
        await self.session.refresh(task)
        # Convert UUID to string immediately to avoid lazy loading issues
        return {"status": "success", "result": {"task_id": str(task.id), "title": task.title, "description": task.description or ""}}

    async def _execute_list_tasks(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        user_id = arguments.get("user_id")
        status = arguments.get("status", "all")
        query = select(Task).where(Task.user_id == user_id)
        
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
            
        # Use exec() for SQLModel instead of execute()
        result = await self.session.exec(query)
        tasks = result.all()
        # Immediately convert to dict to prevent lazy-loading issues
        # Access all attributes while session is active
        task_list = []
        for t in tasks:
            task_list.append({
                "id": str(t.id),
                "title": t.title,
                "description": t.description or "",
                "completed": t.completed
            })
        return {
            "status": "success", 
            "result": {"tasks": task_list}
        }

    async def _execute_delete_task(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        user_id = arguments.get("user_id")
        task_id = arguments.get("task_id")
        title = arguments.get("title")

        query = select(Task).where(Task.user_id == user_id)
        if task_id:
            # Convert string task_id to UUID if needed
            from uuid import UUID
            try:
                task_uuid = UUID(task_id) if isinstance(task_id, str) else task_id
                query = query.where(Task.id == task_uuid)
            except ValueError:
                return {"status": "error", "error": f"Invalid task_id format: {task_id}"}
        elif title:
            # Flexible matching to handle typos
            query = query.where(Task.title.ilike(f"%{title}%"))
        else:
            return {"status": "error", "error": "Either task_id or title must be provided"}
        
        # Use exec() for SQLModel instead of execute()
        result = await self.session.exec(query)
        task = result.first()

        if not task:
            return {"status": "error", "error": f"Task matching '{title or task_id}' not found."}

        # Store task data before deletion (access while session is active)
        res = {"task_id": str(task.id), "title": task.title}
        await self.session.delete(task)
        # Use flush instead of commit - let router handle final commit
        await self.session.flush()
        return {"status": "success", "result": res}

    async def _execute_complete_task(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        user_id = arguments.get("user_id")
        task_id = arguments.get("task_id")
        title = arguments.get("title")

        query = select(Task).where(Task.user_id == user_id)
        if task_id:
            # Convert string task_id to UUID if needed
            from uuid import UUID
            try:
                task_uuid = UUID(task_id) if isinstance(task_id, str) else task_id
                query = query.where(Task.id == task_uuid)
            except ValueError:
                return {"status": "error", "error": f"Invalid task_id format: {task_id}"}
        elif title:
            query = query.where(Task.title.ilike(f"%{title}%"))
        else:
            return {"status": "error", "error": "Either task_id or title must be provided"}
        
        # Use exec() for SQLModel instead of execute()
        result = await self.session.exec(query)
        task = result.first()

        if not task:
            return {"status": "error", "error": f"Task '{title or task_id}' not found."}

        # Check if already completed
        if task.completed:
            return {"status": "success", "result": {"task_id": str(task.id), "title": task.title, "completed": True, "message": "Task was already completed"}}

        task.completed = True
        task.updated_at = datetime.now()
        # Use flush instead of commit - let router handle final commit
        await self.session.flush()
        # Access task attributes while session is active
        return {"status": "success", "result": {"task_id": str(task.id), "title": task.title, "completed": True}}

    async def _execute_update_task(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        user_id = arguments.get("user_id")
        task_id = arguments.get("task_id")
        title = arguments.get("title")
        description = arguments.get("description")

        # Validate that at least one field is being updated
        if not title and description is None:
            return {"status": "error", "error": "Either title or description must be provided"}

        if not task_id:
            return {"status": "error", "error": "task_id is required"}

        query = select(Task).where(Task.user_id == user_id)
        
        # Convert string task_id to UUID if needed
        from uuid import UUID
        try:
            task_uuid = UUID(task_id) if isinstance(task_id, str) else task_id
            query = query.where(Task.id == task_uuid)
        except ValueError:
            return {"status": "error", "error": f"Invalid task_id format: {task_id}"}
        
        result = await self.session.exec(query)
        task = result.first()
        
        if not task:
            return {"status": "error", "error": f"Task with id '{task_id}' not found."}

        # Update fields if provided
        if title:
            task.title = title
        if description is not None:
            task.description = description
        task.updated_at = datetime.now()
        
        await self.session.flush()
        return {"status": "success", "result": {"task_id": str(task.id), "title": task.title, "status": "updated"}}
        