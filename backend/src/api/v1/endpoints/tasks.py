import logging
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID
from src.database.models import TaskCreateRequest, TaskUpdateRequest, TaskResponse
from src.database.repositories import TaskRepository
from src.database.session import get_db_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.middleware.jwt import get_current_user

# Get logger for this module
logger = logging.getLogger(__name__)

# Router configuration
router = APIRouter(prefix="", tags=["tasks"])


# ============================================================================
# DEPENDENCY FUNCTIONS - Reusable logic extracted from endpoints
# ============================================================================

async def verify_user_access(
    user_id: str,
    current_user: dict = Depends(get_current_user)
) -> str:
    """
    Dependency to verify that the authenticated user matches the path user_id.

    Args:
        user_id: User ID from path parameter
        current_user: The authenticated user from Better Auth session

    Returns:
        str: The verified user_id

    Raises:
        HTTPException: 401 if session is invalid, 403 if user doesn't match
    """
    session_user_id = current_user.get("user", {}).get("id")

    if not session_user_id:
        logger.warning("Invalid session: missing user ID")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session: missing user ID"
        )

    if session_user_id != user_id:
        logger.warning(
            f"Access denied: session user {session_user_id} attempting to access {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )

    return user_id


def validate_task_id(task_id: str) -> UUID:
    """
    Dependency to validate and convert task_id string to UUID.
    
    Args:
        task_id: Task ID string from path parameter
        
    Returns:
        UUID: Validated UUID object
        
    Raises:
        HTTPException: 400 if task_id is not a valid UUID
    """
    try:
        return UUID(task_id)
    except ValueError:
        logger.warning(f"Invalid UUID format for task ID: {task_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format. Must be a valid UUID."
        )


# ============================================================================
# ENDPOINT HANDLERS
# ============================================================================

@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    verified_user_id: str = Depends(verify_user_access),
    db: AsyncSession = Depends(get_db_session)
) -> List[TaskResponse]:
    """
    Retrieve all tasks for the authenticated user.

    Args:
        verified_user_id: User ID verified by dependency
        db: Database session dependency

    Returns:
        List[TaskResponse]: List of tasks belonging to the user
        
    Raises:
        HTTPException: 500 if database operation fails
    """
    logger.info(f"Retrieving tasks for user: {verified_user_id}")
    
    try:
        repository = TaskRepository(db)
        tasks = await repository.get_tasks_by_user_id(verified_user_id)
        
        logger.info(f"Successfully retrieved {len(tasks)} tasks for user {verified_user_id}")
        
        # Convert SQLModel tasks to response models
        return [
            TaskResponse(
                id=str(task.id),
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]
        
    except Exception as e:
        logger.error(f"Error retrieving tasks for user {verified_user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks. Please try again later."
        )


@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    request: TaskCreateRequest,
    verified_user_id: str = Depends(verify_user_access),
    db: AsyncSession = Depends(get_db_session)
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    Args:
        request: Task creation request data
        verified_user_id: User ID verified by dependency
        db: Database session dependency

    Returns:
        TaskResponse: The created task with generated ID and timestamps
        
    Raises:
        HTTPException: 500 if task creation fails
    """
    logger.info(
        f"Creating new task for user {verified_user_id} with title: '{request.title}'"
    )
    
    try:
        repository = TaskRepository(db)
        created_task = await repository.create_task_for_user(verified_user_id, request)
        
        logger.info(
            f"Successfully created task {created_task.id} for user {verified_user_id}"
        )
        
        return TaskResponse(
            id=str(created_task.id),
            title=created_task.title,
            description=created_task.description,
            completed=created_task.completed,
            created_at=created_task.created_at,
            updated_at=created_task.updated_at
        )
        
    except Exception as e:
        logger.error(
            f"Error creating task for user {verified_user_id}: {str(e)}", 
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task. Please try again later."
        )


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    request: TaskUpdateRequest,
    task_uuid: UUID = Depends(validate_task_id),
    verified_user_id: str = Depends(verify_user_access),
    db: AsyncSession = Depends(get_db_session)
) -> TaskResponse:
    """
    Update an existing task for the authenticated user.

    Args:
        request: Task update request data
        task_uuid: Validated task UUID from dependency
        verified_user_id: User ID verified by dependency
        db: Database session dependency

    Returns:
        TaskResponse: The updated task
        
    Raises:
        HTTPException: 404 if task not found, 500 if update fails
    """
    logger.info(f"Updating task {task_uuid} for user {verified_user_id}")
    
    try:
        repository = TaskRepository(db)
        updated_task = await repository.update_task_for_user(
            verified_user_id, 
            task_uuid, 
            request
        )
        
        if not updated_task:
            logger.warning(
                f"Task {task_uuid} not found or doesn't belong to user {verified_user_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or you don't have permission to modify it"
            )
        
        logger.info(f"Successfully updated task {task_uuid} for user {verified_user_id}")
        
        return TaskResponse(
            id=str(updated_task.id),
            title=updated_task.title,
            description=updated_task.description,
            completed=updated_task.completed,
            created_at=updated_task.created_at,
            updated_at=updated_task.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error updating task {task_uuid} for user {verified_user_id}: {str(e)}", 
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task. Please try again later."
        )


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_uuid: UUID = Depends(validate_task_id),
    verified_user_id: str = Depends(verify_user_access),
    db: AsyncSession = Depends(get_db_session)
) -> None:
    """
    Delete a task for the authenticated user.

    Args:
        task_uuid: Validated task UUID from dependency
        verified_user_id: User ID verified by dependency
        db: Database session dependency

    Returns:
        None: Returns 204 No Content on successful deletion
        
    Raises:
        HTTPException: 404 if task not found, 500 if deletion fails
    """
    logger.info(f"Deleting task {task_uuid} for user {verified_user_id}")
    
    try:
        repository = TaskRepository(db)
        success = await repository.delete_task_for_user(verified_user_id, task_uuid)
        
        if not success:
            logger.warning(
                f"Task {task_uuid} not found or doesn't belong to user {verified_user_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or you don't have permission to delete it"
            )
        
        logger.info(f"Successfully deleted task {task_uuid} for user {verified_user_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error deleting task {task_uuid} for user {verified_user_id}: {str(e)}", 
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task. Please try again later."
        )