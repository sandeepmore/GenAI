from pathlib import Path
from langchain.mcp import MCPAdapter
from fastmcp.client.transports import PythonStdioTransport
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from fastmcp.client import Client
from fastmcp.client.group import ClientGroup

# from langchain.mcp import LangChainBetaWarning
# warnings.filterwarnings("ignore", category=LangChainBetaWarning)

from dotenv import load_dotenv
load_dotenv()


async def main():
    all_tools = []
    server_status = {}

    # -- 1. Local CineBot (verified by a real run when this notebook was authored) --
    try:
        cinebot_transport = PythonStdioTransport(
            script_path=Path("cinebot_mcp_server.py"),
            log_file=Path("cinebot_mcp_server.log"),
        )
        async with MCPAdapter(cinebot_transport) as adapter:
            tools = await adapter.list_tools()
            all_tools.extend(tools)
            server_status["cinebot (local)"] = f"OK -- {[t.name for t in tools]}"

    except Exception as e:
        server_status["cinebot (local)"] = f"FAILED -- {type(e).__name__}: {e}"

    for name, status in server_status.items():
        print(f"{name}: {status}")

    
    # -- 2. Context7 (free, public, documented to work keyless at lower rate limits) --
    # https://mcp.context7.com/mcp -- pass CONTEXT7_API_KEY as a bearer token if you have one, for
    # higher rate limits; works without one for a quick demo.
    # context7_key = os.environ.get("ctx7sk-f2759f35-1622-4f4c-9a8a-d4691b9039bf")
    context7_key = "ctx7sk-f2759f35-1622-4f4c-9a8a-d4691b9039bf"
    try:
        context7_client = (
            Client("https://mcp.context7.com/mcp", auth=context7_key)
            if context7_key
            else Client("https://mcp.context7.com/mcp")
        )
        async with MCPAdapter(context7_client) as context7_adapter:
            tools = await context7_adapter.list_tools()
            all_tools.extend(tools)
            server_status["context7 (remote, free)"] = f"OK -- {[t.name for t in tools]}"
    except Exception as e:
        server_status["context7 (remote, free)"] = f"FAILED -- {type(e).__name__}: {e}"

    print(f"context7 (remote, free): {server_status['context7 (remote, free)']}")

    # -- 3. Your own remote server --
    # Swap this URL for your own deployment. No API key assumed here -- add one via `auth=` the same
    # way as the Context7 cell above if your server needs it.
    TIMETRACK_URL = "https://time-track-mcp-server.vercel.app/mcp/"

    try:
        async with MCPAdapter(TIMETRACK_URL) as timetrack_adapter:
            tools = await timetrack_adapter.list_tools()
            all_tools.extend(tools)
            server_status["time-track (your remote server)"] = f"OK -- {[t.name for t in tools]}"
    except Exception as e:
        server_status["time-track (your remote server)"] = f"FAILED -- {type(e).__name__}: {e}"

    print(f"time-track (your remote server): {server_status['time-track (your remote server)']}")

    print("\n--- Fleet summary ---")
    for name, status in server_status.items():
        print(f"{name}: {status}")
    print(f"\nTotal tools available to the agent: {len(all_tools)}")

    # Build the agent over whatever connected
    agent = create_agent(model="openai:gpt-5-mini", tools=all_tools)
    print(f"Agent built with {len(all_tools)} tools:", [t.name for t in all_tools])

    # Ask it something -- a tiny input loop
    while True:
        question = input("\nAsk the fleet agent (or 'quit'): ").strip()
        if question.lower() in {"quit", "exit", ""}:
            break
        try: 
            result = await agent.ainvoke({"messages": [("user", question)]})
            for msg in result["messages"]:
                if getattr(msg, "tool_calls", None):
                    for tc in msg.tool_calls:
                        print(f"  [tool call] {tc['name']}({tc['args']})")
            print("Agent:", result["messages"][-1].content)
        except Exception as e:
            print(f"Call skipped -- {type(e).__name__}: {e}")
            
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())