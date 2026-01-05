"""Chat API router for the Todo AI Chatbot application."""
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional, Dict, Any, List
from datetime import datetime
import json

from src.database.engine import get_async_session
from src.services.conversation_service import ConversationService
from src.services.ai_agent_service import AIAgentService
from src.services.tool_execution_service import ToolExecutionService
from src.models.chat_models import ChatRequest, ChatResponse, ToolCall
from src.models.message import MessageCreate, MessageRole
from src.config import settings
from src.utils.logging import app_logger
from src.utils.errors import InvalidRequestError


router = APIRouter(tags=["chat"])


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str = Path(..., description="The ID of the requesting user", min_length=1),
    chat_request: ChatRequest = None,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Chat endpoint that orchestrates AI agent interactions with tools, 
    persists data, and handles errors safely.
    """
    if not chat_request:
        raise InvalidRequestError("Request body is required", field="request_body")

    conversation_service = ConversationService(session)
    ai_agent_service = AIAgentService(api_key=settings.google_ai_api_key)
    
    conversation_id = chat_request.conversation_id
    user_message = chat_request.message
    
    try:
        # 1. Initialize or load conversation
        if conversation_id is None:
            title = f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            conversation = await conversation_service.create_conversation(user_id, title)
            conversation_id = conversation.id
        else:
            conversation = await conversation_service.get_conversation(conversation_id, user_id)
        
        # 2. Fetch history and store user message
        conversation_history = await conversation_service.get_conversation_history(conversation_id, user_id)
        
        user_message_data = MessageCreate(
            conversation_id=conversation_id,
            user_id=user_id,
            role=MessageRole.user,
            content=user_message
        )
        await conversation_service.create_message(user_message_data)
        
        # 3. Build message array for AI
        ai_messages = []
        for msg in conversation_history:
            ai_messages.append({
                "role": msg.role.value,
                "content": msg.content
            })
        
        # 4. Define MCP tools (Updated with title support)
        mcp_tools_config = {
            "add_task": {
                "description": "Add a new task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["title"]
                }
            },
            "list_tasks": {
                "description": "List all tasks. Status: 'all', 'pending', 'completed'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                    }
                }
            },
            "complete_task": {
                "description": "Complete a task. Use task_id OR title.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "title": {"type": "string"}
                    }
                }
            },
            "delete_task": {
                "description": "Delete a task. Use task_id OR title.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "title": {"type": "string"}
                    }
                }
            },
            "update_task": {
                "description": "Update a task's title or description. Use task_id (UUID string) and optionally title and/or description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The task ID (UUID) to update"},
                        "title": {"type": "string", "description": "New title for the task"},
                        "description": {"type": "string", "description": "New description for the task"}
                    },
                    "required": ["task_id"]
                }
            }
        }

        # 5. Process with AI
        ai_response = await ai_agent_service.process_message_with_mcp_tools(
            user_message=user_message,
            conversation_history=ai_messages,
            mcp_tools_config=mcp_tools_config
        )
        
        response_text = ai_response["response"]
        tool_calls = ai_response["tool_calls"]
        executed_tool_calls = []

        # 6. Execute Tools & Sanitize Results
        if tool_calls:
            tool_service = ToolExecutionService(session)
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                arguments = tool_call["args"]
                arguments["user_id"] = user_id

                result = await tool_service.execute_tool(tool_name, arguments)
                
                # SANITIZATION: Ensure result is serializable to avoid Greenlet/JSON errors
                clean_result = result["result"] if result["status"] == "success" else {"error": result["error"]}
                if isinstance(clean_result, dict):
                    clean_result = {k: str(v) for k, v in clean_result.items()}

                executed_tool_calls.append({
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "result": clean_result
                })
            
            # Get final AI response after tool execution
            ai_messages.append({"role": "assistant", "content": response_text})
            for call in executed_tool_calls:
                ai_messages.append({
                    "role": "user",
                    "content": f"Tool {call['tool_name']} result: {call['result']}"
                })
            
            final_ai = await ai_agent_service.process_message_with_mcp_tools(
                user_message="",
                conversation_history=ai_messages,
                mcp_tools_config=mcp_tools_config
            )
            response_text = final_ai["response"]

        # 7. Store Assistant Message & Commit
        assistant_message_data = MessageCreate(
            conversation_id=conversation_id,
            user_id=user_id,
            role=MessageRole.assistant,
            content=response_text,
            tool_calls={"calls": executed_tool_calls} if executed_tool_calls else None
        )
        await conversation_service.create_message(assistant_message_data)
        await conversation_service.update_conversation_timestamp(conversation_id)
        
        await session.commit()
        
        return ChatResponse(
            conversation_id=conversation_id,
            response=response_text,
            tool_calls=[ToolCall(**call) for call in executed_tool_calls]
        )
        
    except Exception as e:
        # CRITICAL: Rollback on error to prevent session poisoning
        await session.rollback()
        app_logger.error(f"Chat error: {str(e)}", user_id=user_id)
        raise HTTPException(
            status_code=500,
            detail={"error": "INTERNAL_ERROR", "message": "An unexpected error occurred."}
        )