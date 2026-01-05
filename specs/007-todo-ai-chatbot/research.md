# Research: Todo AI Chatbot - Database Schema for Conversations

## Decision: Database Technology Choice
**Rationale**: Using PostgreSQL as it's already part of the tech stack (as evidenced by the existing 004-neon-database feature) and provides excellent JSONB support for storing tool_calls data. PostgreSQL offers the necessary features for this implementation: foreign keys, cascading deletes, indexing options, and JSON operations.

**Alternatives considered**:
- SQLite: Simpler but lacks advanced JSON operations
- MongoDB: Better for document storage but doesn't fit the existing relational pattern
- MySQL: Similar capabilities but PostgreSQL has superior JSON support

## Decision: ORM Framework
**Rationale**: Using SQLAlchemy/SQLModel as it's compatible with FastAPI (which is part of the existing stack from the 006-better-auth-integration feature) and provides the right balance of abstraction and control. SQLModel is particularly good as it integrates Pydantic models with SQLAlchemy.

**Alternatives considered**:
- Peewee: Simpler ORM but less feature-rich
- Tortoise ORM: Async-native but doesn't integrate as well with existing code
- Raw SQL: More control but less maintainable

## Decision: Conversation Relationship Design
**Rationale**: Implementing a parent-child relationship between conversations and messages with proper foreign keys and cascade delete ensures data integrity. The user_id duplication in the messages table enables efficient user-based queries without joins.

**Alternatives considered**:
- Single table with hierarchy: Would be less efficient for queries
- Document-based approach: Would lose relational benefits
- Separate user verification: Would require additional joins for security checks

## Decision: Message Role Constraints
**Rationale**: Using a database-level check constraint to limit message roles to 'user', 'assistant', or 'system' ensures data integrity at the source. This prevents invalid role values from being stored.

**Alternatives considered**:
- Application-level validation only: Less reliable as it could be bypassed
- Database enum type: More rigid and harder to modify later
- String validation only: Less strict than check constraints

## Decision: Indexing Strategy
**Rationale**: Creating indexes on user_id, conversation_id, and timestamps enables efficient querying patterns expected in the application. The updated_at index on conversations supports sorting recent conversations, while conversation_id and created_at on messages support chronological retrieval.

**Alternatives considered**:
- No indexes: Would cause performance issues
- All-field indexes: Would waste storage and slow down writes
- Composite indexes: Considered but single-field indexes are more flexible for various query patterns

## Decision: JSONB for Tool Calls
**Rationale**: Using JSONB for tool_calls field provides flexibility to store various MCP tool call structures while still allowing for querying when needed. PostgreSQL's JSONB offers good performance and features.

**Alternatives considered**:
- Separate tool_calls table: Would complicate queries
- JSON (not JSONB): Less efficient for querying
- Fixed schema columns: Too rigid for varying tool call structures