"""
MCP Server Core Implementation

This module implements the core MCP server functionality that exposes standardized tools
for AI agents to interact with the task management system.
"""
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel


class MCPTaskInput(BaseModel):
    """Base class for MCP task inputs"""
    user_id: str


class MCPTaskOutput(BaseModel):
    """Base class for MCP task outputs"""
    status: str


class MCPTask(ABC):
    """Abstract base class for MCP tools"""

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the MCP tool with given input data"""
        pass

    @abstractmethod
    def get_input_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's input"""
        pass

    @abstractmethod
    def get_output_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's output"""
        pass


class MCPToolRegistry:
    """Registry for MCP tools"""

    def __init__(self):
        self._tools: Dict[str, MCPTask] = {}

    def register_tool(self, name: str, tool: MCPTask):
        """Register an MCP tool"""
        self._tools[name] = tool

    def get_tool(self, name: str) -> MCPTask:
        """Get an MCP tool by name"""
        return self._tools.get(name)

    def get_all_tools(self) -> List[Dict[str, Any]]:
        """Get all registered tools with their schemas"""
        tools_list = []
        for name, tool in self._tools.items():
            tools_list.append({
                "name": name,
                "description": getattr(tool, '__doc__', f'MCP tool for {name}') or f'MCP tool for {name}',
                "input_schema": tool.get_input_schema(),
                "output_schema": tool.get_output_schema()
            })
        return tools_list

    def list_tool_names(self) -> List[str]:
        """List all registered tool names"""
        return list(self._tools.keys())


# Global registry instance
mcp_registry = MCPToolRegistry()


class MCPServer:
    """Main MCP Server class"""

    def __init__(self):
        self.registry = mcp_registry

    def register_tool(self, name: str, tool: MCPTask):
        """Register a tool with the server"""
        self.registry.register_tool(name, tool)

    def get_tool(self, name: str) -> MCPTask:
        """Get a tool by name"""
        return self.registry.get_tool(name)

    def list_all_tools(self) -> List[Dict[str, Any]]:
        """List all available tools with schemas"""
        return self.registry.get_all_tools()

    def get_tool_names(self) -> List[str]:
        """Get list of all tool names"""
        return self.registry.list_tool_names()


# Global server instance
mcp_server = MCPServer()