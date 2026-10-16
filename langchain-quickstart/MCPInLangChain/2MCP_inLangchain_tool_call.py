from pathlib import Path
from langchain.mcp import MCPAdapter
from fastmcp.client.transports import PythonStdioTransport
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

cinebot_mcp_transport = PythonStdioTransport(
    script_path=Path("./cinebot_mcp_server.py"),
    log_file=Path("cinebot_mcp_server.log")
)


async def main():
    tool_call_result=''
    async with MCPAdapter(cinebot_mcp_transport) as adapter:
        tools = await adapter.list_tools()

        showtime_tool = next((t for t in tools if t.name == "check_showtimes"), None)

        direct_result = await showtime_tool.ainvoke({"movie_title": "interstellar"})
        print("Direct invocation result:", direct_result)
        # O/P:
        # Direct invocation result: [{'type': 'text', 'text': '7:00 PM and 10:15 PM', 'id': 'lc_2db5f8d8-a103-45ad-916f-a126fb1da4a9'}]

    # Calling with Agent as well

        try:
            cinebot_agent = create_agent(model='openai:gpt-5-mini',tools=tools)
            result = await cinebot_agent.ainvoke({"messages":[('user', "What are the showtimes for Interstellar?")]})
            tool_call_result = result
            # from rich import print as rprint
            # rprint("[bold green]Direct tool invocation result:[/bold green]", tool_call_result)
            print("Agent invocation result:", tool_call_result['messages'][-1])
        except Exception as e:
            print("Error during agent invocation:", e)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())