# Quickstart Guide: Task Backend API (Frontend Integration Only)

## Prerequisites

- Python 3.11+ installed
- pip package manager
- Virtual environment tool (venv, conda, etc.)

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install production dependencies
pip install fastapi uvicorn python-multipart pydantic

# Install development dependencies (optional)
pip install pytest httpx
```

### 3. Project Structure

After setup, your project should have this structure:

```
backend/
├── src/
│   ├── main.py
│   ├── models/
│   │   └── task.py
│   ├── schemas/
│   │   └── task.py
│   ├── database/
│   │   └── memory_db.py
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── tasks.py
│   └── core/
│       └── config.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

### 4. Key Implementation Files

#### Task Model (`src/models/task.py`)

```python
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
```

#### Task Schemas (`src/schemas/task.py`)

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None

    @field_validator('title')
    def validate_title(cls, v):
        if not v or len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator('title')
    def validate_title(cls, v):
        if v is not None and (len(v) < 1 or len(v) > 200):
            raise ValueError('Title must be between 1 and 200 characters')
        return v

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

class ErrorResponse(BaseModel):
    error: str
```

#### In-Memory Database (`src/database/memory_db.py`)

```python
from typing import Dict, List, Optional
from src.models.task import Task

class InMemoryTaskDB:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def get_all_tasks(self) -> List[Task]:
        return list(self._tasks.values())

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def create_task(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def update_task(self, task_id: str, task: Task) -> Optional[Task]:
        if task_id in self._tasks:
            self._tasks[task_id] = task
            return task
        return None

    def delete_task(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

# Global instance
db = InMemoryTaskDB()
```

#### Tasks API Endpoints (`src/api/v1/endpoints/tasks.py`)

```python
from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.task import Task
from src.schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskResponse, ErrorResponse
from src.database.memory_db import db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskResponse])
async def get_tasks() -> List[TaskResponse]:
    tasks = db.get_all_tasks()
    return [TaskResponse.model_validate(task) for task in tasks]

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(request: TaskCreateRequest) -> TaskResponse:
    task = Task.create(title=request.title, description=request.description)
    created_task = db.create_task(task)
    return TaskResponse.model_validate(created_task)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, request: TaskUpdateRequest) -> TaskResponse:
    existing_task = db.get_task(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task with provided values
    if request.title is not None:
        existing_task.title = request.title
    if request.description is not None:
        existing_task.description = request.description
    if request.completed is not None:
        existing_task.completed = request.completed

    existing_task.updated_at = datetime.now()
    updated_task = db.update_task(task_id, existing_task)

    return TaskResponse.model_validate(updated_task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    success = db.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return
```

#### Main Application (`src/main.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints.tasks import router as tasks_router
from src.core.config import settings

app = FastAPI(
    title="Task Backend API",
    description="Backend API for task management frontend integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(tasks_router)

@app.get("/")
async def root():
    return {"message": "Task Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 5. Running the Application

```bash
# Development mode
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# The API will be available at http://localhost:8000
# OpenAPI docs at http://localhost:8000/docs
```

### 6. Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run API tests
pytest tests/api/
```

### 7. Frontend Integration

To connect your existing frontend Todo application to this backend:

1. Update the frontend service/api calls to point to your backend endpoints
2. Replace local state operations with HTTP requests to the backend
3. Handle the API responses and errors appropriately

Example API calls from frontend:
```javascript
// Fetch all tasks
fetch('http://localhost:8000/tasks')
  .then(response => response.json())
  .then(tasks => console.log(tasks));

// Create a new task
fetch('http://localhost:8000/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'New task',
    description: 'Task description'
  })
})
  .then(response => response.json())
  .then(task => console.log(task));
```

## Environment Configuration

Create a `.env` file in the backend root for configuration:

```
# Server configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
SERVER_RELOAD=true

# CORS configuration
FRONTEND_URL=http://localhost:3000  # Your frontend URL
```

## Troubleshooting

- **API not responding**: Ensure the server is running and check the port
- **CORS errors**: Verify frontend origin is allowed in CORS middleware
- **Validation errors**: Check that request bodies match the API contract
- **Task not found**: Verify the task ID exists and is properly formatted as UUID