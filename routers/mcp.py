# MCP Router - Handles MCP server information and management
from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
from shared.state import get_multi_mcp

router = APIRouter(prefix="/mcp", tags=["MCP"])

# Get shared instance
multi_mcp = get_multi_mcp()


@router.get("/servers")
async def get_servers():
    """Get information about all configured MCP servers"""
    try:
        servers_info = {}
        
        # Get connected servers
        connected = multi_mcp.get_connected_servers()
        
        # Get server configs
        for server_name, config in multi_mcp.server_configs.items():
            tools = multi_mcp.tools.get(server_name, [])
            
            servers_info[server_name] = {
                "name": server_name,
                "enabled": config.get("enabled", True),
                "type": config.get("type", "local-script"),
                "connected": server_name in connected,
                "tools_count": len(tools),
                "tools": [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.inputSchema
                    }
                    for tool in tools
                ],
                "config": {
                    "command": config.get("command"),
                    "args": config.get("args", [])[:3]  # First few args only
                }
            }
        
        return servers_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get MCP servers: {str(e)}")


@router.get("/servers/{server_name}/tools")
async def get_server_tools(server_name: str):
    """Get tools for a specific server"""
    try:
        if server_name not in multi_mcp.tools:
            raise HTTPException(status_code=404, detail=f"Server '{server_name}' not found")
        
        tools = multi_mcp.tools[server_name]
        return {
            "server": server_name,
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema
                }
                for tool in tools
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tools: {str(e)}")


@router.get("/tools")
async def get_all_tools():
    """Get all tools from all servers"""
    try:
        all_tools = multi_mcp.get_all_tools()
        return {
            "total": len(all_tools),
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema
                }
                for tool in all_tools
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tools: {str(e)}")

