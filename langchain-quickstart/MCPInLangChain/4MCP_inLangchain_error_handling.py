from pathlib import Path
from langchain.mcp import MCPAdapter
from fastmcp.client.transports import PythonStdioTransport
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

error_message_global = ''
error_transport = PythonStdioTransport(
    script_path=Path('cinebot_error_server.py'),
    log_file=Path('cinebot_error_server1.log')
)

async def main():
    tool_call_result=''
    async with MCPAdapter(error_transport) as mcp_adapter:
        tools = await mcp_adapter.list_tools()
        risky_lookup_tool = tools[0]

        bad_call = {
            'name': 'risky_lookup', 
            'args': {'booking_id': '12345'}, 
            'id': 'bad_call_001', 
            'type': 'tool_call'
        }

        error_message = await risky_lookup_tool.ainvoke(bad_call)
        print("Error message from tool:", error_message)
        print("Content:", error_message.content)
        error_message_global = error_message
        print(error_message)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())