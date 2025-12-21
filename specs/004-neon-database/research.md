# Research: Neon Database Integration

**Feature**: Neon Database Integration | **Date**: 2025-12-16 | **Plan**: [specs/004-neon-database/plan.md](specs/004-neon-database/plan.md)

## Decision: Use SQLModel with PostgreSQL for Neon Database

**Rationale**: SQLModel is the recommended library by FastAPI creator, combines Pydantic validation with SQLAlchemy ORM capabilities, and provides excellent support for PostgreSQL. It allows using the same models for both database operations and API schemas, reducing code duplication.

**Alternatives considered**:
1. Pure SQLAlchemy ORM - More complex setup, separate validation layer needed
2. Tortoise ORM - Async native but less mature ecosystem
3. Databases + SQLAlchemy Core - More manual work, less type safety
4. Prisma with Python - Not well supported in Python ecosystem

## Decision: Use Connection Pooling with asyncpg

**Rationale**: asyncpg provides excellent performance for PostgreSQL with asyncio, and when combined with SQLAlchemy's connection pooling, provides efficient database connection management for concurrent requests.

**Alternatives considered**:
1. psycopg3 - Newer but less proven in production
2. aiopg - Based on older asyncio patterns
3. Pure sync connections - Would block the event loop

## Decision: Use Alembic for Database Migrations

**Rationale**: Alembic is the standard migration tool for SQLAlchemy-based applications and integrates well with SQLModel. It provides automatic migration generation and version control for database schema changes.

**Alternatives considered**:
1. Flask-Migrate - Designed for Flask applications
2. Manual migrations - Error-prone and difficult to maintain
3. Django migrations - Not applicable to FastAPI applications

## Neon Database Specific Considerations

### Connection String Format
Neon database connection string follows PostgreSQL format:
`postgresql+asyncpg://username:password@ep-xxx-neondb.region.provider.neon.tech/dbname?sslmode=require`

### Connection Pooling Settings
- Minimum pool size: 2-5 connections
- Maximum pool size: 20-30 connections depending on expected load
- Connection timeout: 30 seconds
- Idle connection timeout: 300 seconds

### Security Best Practices
- Use environment variables for database credentials
- Enable SSL mode for all connections
- Use role-based access control in Neon
- Implement connection timeout handling

## Implementation Approach

### Database Models
The existing Task model needs to be updated to inherit from SQLModel and include database-specific configurations like table name, field constraints, and relationships.

### Data Access Layer
Create repository pattern or service layer functions that handle database operations for tasks, with proper error handling and transaction management.

### Migration Strategy
1. Create initial migration for existing Task entity
2. Update database connection in main application
3. Replace in-memory database with PostgreSQL operations
4. Maintain API contract compatibility