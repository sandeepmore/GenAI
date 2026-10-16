from pathlib import Path
from langchain.mcp import MCPAdapter
from fastmcp.client.transports import PythonStdioTransport
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from fastmcp.client import Client
from fastmcp.client.group import ClientGroup

from dotenv import load_dotenv
load_dotenv()


group = ClientGroup(
    {
        "cinebot": Client(Path("cinebot_mcp_server.py")),
        "errors": Client(Path("cinebot_error_server.py"),mode="legacy"),
        'time_track_server':Client('https://time-track-mcp-server.vercel.app/mcp/')
    }
)


async def main():
    async with MCPAdapter(group) as adapter:
        group_tools = await adapter.list_tools()
        print("ClientGroup fleet tools:", [t.name for t in group_tools])
        # ClientGroup fleet tools: ['cinebot_check_showtimes', 'cinebot_cancel_booking', 'cinebot_get_seat_map', 'errors_risky_lookup', 'time_track_server_log_time', 'time_track_server_get_timesheet', 'time_track_server_get_project_summary', 'time_track_server_list_projects']

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())