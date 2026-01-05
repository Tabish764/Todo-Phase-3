# ADR: Stateless AI Chat Architecture

## Status
Proposed

## Context
The Todo AI Chatbot application needs to handle conversations with an AI agent (Google Gemini) while maintaining conversation history and supporting MCP tool integration. The architecture must support horizontal scaling, server restarts without losing conversation context, and efficient resource usage.

## Decision
We will implement a completely stateless chat architecture where:

1. **Conversation History Loading**: Full conversation history is loaded from the database before each AI processing call, rather than maintaining in-memory session state.

2. **No Server-Side Session Storage**: No conversation state is stored in server memory, Redis, or any other session storage mechanism between requests.

3. **Database-Driven Context**: All conversation context is retrieved from the database on each request, ensuring that any server instance can handle any request.

4. **Message Persistence**: User and assistant messages are immediately persisted to the database to maintain conversation continuity.

## Alternatives Considered
- **In-Memory Session Storage**: Store conversation context in server memory for faster access but limits horizontal scaling and causes issues on server restarts.
- **Redis Session Storage**: Use Redis to store conversation state but adds infrastructure complexity and potential failure points.
- **Hybrid Approach**: Store recent conversation context in memory with database backup but adds complexity and potential inconsistency.

## Rationale
- **Scalability**: Stateless design allows horizontal scaling without complex session sharing.
- **Resilience**: Server restarts don't lose conversation context.
- **Simplicity**: Single source of truth in the database reduces complexity.
- **Consistency**: All server instances see the same conversation state.

## Consequences
### Positive
- Easy horizontal scaling
- Resilience to server restarts
- Consistent state across all instances
- Simplified deployment

### Negative
- Increased database load with each request
- Potential performance impact from loading full history
- Requires efficient database queries

## Implementation
- `chat_router.py` loads full conversation history from database before AI processing
- `conversation_service.py` provides efficient history retrieval with proper ordering
- Messages are immediately stored in database before and after AI processing
- Conversation timestamps are updated on each interaction