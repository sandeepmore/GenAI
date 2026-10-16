from pathlib import Path
from langchain.mcp import MCPAdapter
from fastmcp.client.transports import PythonStdioTransport

cinebot_mcp_transport = PythonStdioTransport(
    script_path=Path("./cinebot_mcp_server.py"),
    log_file=Path("cinebot_mcp_server.log")
)

async def main():
    async with MCPAdapter(cinebot_mcp_transport) as mcp_adapter:
        # Now you can use the mcp_adapter to interact with the MCP server
        tools=await mcp_adapter.list_tools()
        print("Available tools:", [t.name for t in tools])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())