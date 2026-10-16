from pathlib import Path
from langchain.mcp import MCPAdapter
from fastmcp.client.transports import PythonStdioTransport
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware

from dotenv import load_dotenv
load_dotenv()

elicit_transport = PythonStdioTransport(
    script_path=Path("./cinebot_elicit_server.py"),
    log_file=Path("cinebot_elicit_server.log")
)

def is_destructive_tool_call(tool):
    # return message.type == "tool_call" and message.name == "cancel_booking"
    meta = (tool.metadata or {}).get('mcp',{}).get('tool',{}).get('annotations',{})
    return bool(meta.get('destructive_hint'))

async def main():
    async with MCPAdapter(elicit_transport) as adapter:
        tools = await adapter.list_tools()
        confirm_tool = next(t for t in tools if t.name == "cancel_booking_confirm")
    
        tool_call = {
            "name": "cancel_booking_confirm",
            "args": {"booking_id": "BK123"},
            "id": "call_1",
            "type": "tool_call",
        }
        elicit_result = await confirm_tool.ainvoke(tool_call)
        print("status:", elicit_result.status)
        print("content:", elicit_result.content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())