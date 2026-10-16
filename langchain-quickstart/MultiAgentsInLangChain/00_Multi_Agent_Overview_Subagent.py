import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Copy .env.example to .env in this folder and add your key."
    )

from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-5-mini")
# print("Model ready.")

# Pattern 1: Subagents -- minimal example.
# A supervisor calls specialist agents as tools. The supervisor never sees the specialists'
# internal reasoning or tool calls -- only their final answers.
from langchain.tools import tool
from langchain.agents import create_agent

@tool
def check_seat_availability(showtime: str) -> str:
    """Check how many seats are left for a showtime."""
    return f"{showtime}: 12 seats remaining in Screen 3."

booking_specialist = create_agent(
    model,
    tools=[check_seat_availability],
    system_prompt="You are a booking specialist. Use your tool to answer seat questions.",
)

@tool
def handle_booking_question(request: str) -> str:
    """Delegate a booking-related question to the booking specialist."""
    result = booking_specialist.invoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].content

supervisor = create_agent(
    model,
    tools=[handle_booking_question],
    system_prompt="You are a helpful front-of-house assistant. Delegate booking questions.",
)

result = supervisor.invoke({"messages": [{"role": "user", "content": "How many seats are left for the 7pm Interstellar showing?"}]})
print(result["messages"][-1].content)