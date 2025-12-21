# Quickstart: Neon Database Integration

**Feature**: Neon Database Integration | **Date**: 2025-12-16 | **Plan**: [specs/004-neon-database/plan.md](specs/004-neon-database/plan.md)

## Prerequisites

- Python 3.13+
- Neon Database account and project
- uv package manager
- Existing backend project setup

## Setup Steps

### 1. Create Neon Database
1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Get the connection string from the project dashboard

### 2. Update Dependencies
Add required packages to `backend/requirements.txt`:
```txt
sqlmodel>=0.0.27
asyncpg>=0.30.0
alembic>=1.13.0
```

### 3. Configure Environment
Create/update `.env` file with:
```env
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx-neondb.region.provider.neon.tech/dbname?sslmode=require
```

### 4. Database Setup Code
1. Create database connection module
2. Create SQLModel models
3. Set up Alembic for migrations
4. Update main application to use database session

### 5. Run Migrations
```bash
alembic revision --autogenerate -m "Initial task table"
alembic upgrade head
```

## Development Workflow

### Running the Application
```bash
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

### Running Migrations
```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Check migration status
alembic current
```

### Testing Database Operations
- Use existing test suite to verify database integration
- Test CRUD operations manually via API
- Verify data persistence across application restarts

## API Compatibility
- All existing API endpoints remain unchanged
- Frontend integration continues to work without modifications
- Response formats remain identical to in-memory implementation