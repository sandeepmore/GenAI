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
    async with MCPAdapter(cinebot_mcp_transport) as mcp_adapter:
        tools = await mcp_adapter.list_tools()
        seat_map_tool = next(t for t in tools if t.name == "get_seat_map")
    
        tool_call ={
            'name': 'get_seat_map',
            'args': {'movie_title': 'Interstellar'},
            'id': 'unique_call_id_12345',  # Optional: Provide a unique ID for the call
            'type':'tool_call'
        }
    
        message = await seat_map_tool.ainvoke(tool_call)
        print("Text Content (what my model reads)",message.content)
        # Text Content (what my model reads) [{'type': 'text', 'text': '{"movie":"Interstellar","available_rows":["A","B","C"],"sold_out_rows":["D"]}', 'id': 'lc_f800cb89-7266-448a-bcf3-297ee9dd86ea'}]

        print("Structured Data (what my code can use if required)",message.artifact)
        # Structured Data (what my code can use if required) {'structured_content': {'movie': 'Interstellar', 'available_rows': ['A', 'B', 'C'], 'sold_out_rows': ['D']}}

        print(message.artifact['structured_content'])
        # {'movie': 'Interstellar', 'available_rows': ['A', 'B', 'C'], 'sold_out_rows': ['D']}

        print(message.artifact['structured_content']['available_rows'])  # Accessing structured data directly
        # ['A', 'B', 'C']

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())