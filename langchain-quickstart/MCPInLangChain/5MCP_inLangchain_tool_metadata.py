from pathlib import Path
from langchain.mcp import MCPAdapter
from fastmcp.client.transports import PythonStdioTransport
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware

from dotenv import load_dotenv
load_dotenv()

cinebot_transport = PythonStdioTransport(
    script_path=Path("./cinebot_mcp_server.py"),
    log_file=Path("cinebot_mcp_server.log")
)

def is_destructive_tool_call(tool):
    # return message.type == "tool_call" and message.name == "cancel_booking"
    meta = (tool.metadata or {}).get('mcp',{}).get('tool',{}).get('annotations',{})
    return bool(meta.get('destructive_hint'))

async def main():
    async with MCPAdapter(cinebot_transport) as adapter:
        tools = await adapter.list_tools()

        for t in tools:
            print(f"{t.name}: destructive={is_destructive_tool_call(t)}")

        # check_showtimes: destructive=False
        # cancel_booking: destructive=True
        # get_seat_map: destructive=False

        # One HITL config, built dynamically from whatever the server marked destructive.
        interrupt_on = {
            t.name: {"allowed_decisions": ["approve", "edit", "reject"]}
            for t in tools
            if is_destructive_tool_call(t)
        }
        print("\ninterrupt_on config:", interrupt_on)
        # interrupt_on config: {'cancel_booking': {'allowed_decisions': ['approve', 'edit', 'reject']}}

        hitl_middleware = HumanInTheLoopMiddleware(interrupt_on=interrupt_on)
        cinebot_guarded = create_agent(model="openai:gpt-5-mini", tools=tools, middleware=[hitl_middleware])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())