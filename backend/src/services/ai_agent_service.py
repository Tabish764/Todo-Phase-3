"""AI Agent service for the Todo AI Chatbot application using Gemini API with OpenAI SDK."""
import os
import asyncio
from typing import Dict, Any, List, Optional
from openai import OpenAI
from src.utils.errors import AIServiceError
from src.utils.logging import app_logger


class AIAgentService:
    """Service class for interacting with AI models."""

    def __init__(self, api_key: Optional[str] = None):
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        # Initialize the OpenAI client pointing to Gemini API
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        # Use Gemini model with OpenAI-compatible endpoint
        self.model = "gemini-2.5-flash"

        # Store MCP tools configuration
        self.mcp_tools = {}

    def set_mcp_tools(self, tools_config: Dict[str, Any]):
        """Set the MCP tools configuration."""
        self.mcp_tools = tools_config

    async def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        available_tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Process a user message and return AI response."""
        try:
            # Prepare the messages array for the OpenAI API
            messages = []

            # Add system instructions for the first message
            if not conversation_history:
                messages.append({
                    "role": "system",
                    "content": "You are a helpful AI assistant that helps users manage their tasks. You can interact with task management tools when needed. Only use tools when the user explicitly asks to add, list, complete, update, or delete tasks."
                })

            # Add conversation history
            for msg in conversation_history:
                role = msg.get("role", "user")
                content = msg.get("content", "")

                # Handle messages that might have tool call information
                if isinstance(content, dict) and "role" in content and "parts" in content:
                    # This is likely a Google format - convert to OpenAI format
                    content = content.get("parts", [""])[0] if content.get("parts") else ""

                messages.append({
                    "role": role,
                    "content": content
                })

            # Add the current user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Prepare tools for function calling
            tools = available_tools or []

            # Call the Gemini API using OpenAI SDK in a thread to avoid blocking
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None,
                temperature=0.7,
                max_tokens=1024
            )

            # Extract the response
            choice = response.choices[0]
            message = choice.message

            response_text = message.content if message.content else "I couldn't process that request."

            # Extract tool calls if any
            tool_calls = []
            if message.tool_calls:
                import json
                for tool_call in message.tool_calls:
                    tool_call_dict = {
                        "name": tool_call.function.name,
                        "args": json.loads(tool_call.function.arguments),
                        "id": tool_call.id
                    }
                    tool_calls.append(tool_call_dict)

            return {
                "response": response_text,
                "tool_calls": tool_calls
            }

        except Exception as e:
            app_logger.error(f"Error processing AI message: {str(e)}")
            raise AIServiceError(f"Failed to process AI request: {str(e)}")

    async def process_message_with_mcp_tools(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        mcp_tools_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process a message with MCP tools configuration."""
        # Convert MCP tools config to the format expected by the OpenAI model
        available_tools = self._convert_mcp_tools_to_openai_format(mcp_tools_config or {})

        return await self.process_message(
            user_message=user_message,
            conversation_history=conversation_history,
            available_tools=available_tools
        )

    def _convert_mcp_tools_to_openai_format(self, mcp_tools_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert MCP tools configuration to OpenAI format."""
        tools = []

        for tool_name, tool_config in mcp_tools_config.items():
            # Convert to OpenAI tools format
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_config.get("description", ""),
                    "parameters": tool_config.get("parameters", {})
                }
            }
            tools.append(openai_tool)

        return tools