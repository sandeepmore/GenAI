from pathlib import Path
from langchain.mcp import MCPAdapter
from fastmcp.client.transports import PythonStdioTransport
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from fastmcp.mcp_config import MCPConfig

from dotenv import load_dotenv
load_dotenv()


fleet_config: MCPConfig = {
    "mcpServers": {
        "cinebot": {
            "command": "python",
            "args": ["cinebot_mcp_server.py"],
        },
        "errors": {
            "command": "python",
            "args": ["cinebot_error_server.py"],
        },
    }
}

async def main():
    async with MCPAdapter(fleet_config) as adapter:
        fleet_tools = await adapter.list_tools()
        print("MCPConfig fleet tools:", [t.name for t in fleet_tools])
        # MCPConfig fleet tools: ['cinebot_check_showtimes', 'cinebot_cancel_booking', 'cinebot_get_seat_map', 'errors_risky_lookup']

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())