# Data Model: Neon Database Integration

**Feature**: Neon Database Integration | **Date**: 2025-12-16 | **Plan**: [specs/004-neon-database/plan.md](specs/004-neon-database/plan.md)

## Entity: Task

### Database Table: `tasks`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, Default: gen_random_uuid() | Unique identifier for the task |
| `title` | VARCHAR(200) | NOT NULL, CHECK length(1-200) | Task title with validation |
| `description` | TEXT | NULL | Optional task description |
| `completed` | BOOLEAN | NOT NULL, Default: false | Completion status of the task |
| `created_at` | TIMESTAMP | NOT NULL, Default: NOW() | Timestamp when task was created |
| `updated_at` | TIMESTAMP | NOT NULL, Default: NOW() | Timestamp when task was last updated |

### SQLModel Definition
```python
from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Update updated_at on changes
    def __setattr__(self, name, value):
        if name == "updated_at":
            super().__setattr__(name, datetime.now())
        super().__setattr__(name, value)
```

## Database Relationships

### Current State
- The Task entity is standalone with no relationships to other entities
- Future authentication integration may add user relationship

### Indexes
- Primary key index on `id`
- Index on `completed` field for filtering completed tasks
- Composite index on `(completed, created_at)` for common queries

## Validation Rules

### Title Validation
- Length: 1-200 characters (enforced at database and application level)
- Required: Cannot be null or empty string

### Description Validation
- Length: Up to 1000 characters
- Optional: Can be null

### Timestamp Validation
- `created_at`: Auto-generated on creation, read-only
- `updated_at`: Auto-generated on creation and updates

## Migration Plan

### Initial Schema Migration
1. Create `tasks` table with all fields
2. Set up UUID extension for PostgreSQL
3. Configure indexes
4. Set up row-level security (optional, for future authentication)

### Data Migration
- No data migration needed as we're replacing in-memory storage
- Existing in-memory data will be lost (acceptable for this transition)

## API Contract Compatibility

### Request/Response Models
- `TaskCreateRequest`, `TaskUpdateRequest`, and `TaskResponse` schemas remain unchanged
- Only the underlying storage mechanism changes
- All existing API endpoints maintain the same contract