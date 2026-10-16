import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Copy .env.example to .env in this folder and add your key."
    )

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-5-mini")
# print("Model ready.")

# Pattern 3: Skills -- minimal example.
# The agent sees lightweight skill descriptions up front, and loads full content on demand.
SKILLS = {
    "refund_policy": "Full refund if cancelled 2+ hours before showtime; 50% credit within 2 hours.",
}

@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill's full content.

    Available skills:
    - refund_policy: refund and cancellation rules
    """
    return SKILLS.get(skill_name, f"Unknown skill: {skill_name}")

skills_agent = create_agent(
    model,
    tools=[load_skill],
    system_prompt="You are a CineBot assistant. Use load_skill when a question needs policy detail.",
)
result = skills_agent.invoke({"messages": [{"role": "user", "content": "If I cancel 3 hours before the show, do I get a refund?"}]})
print(result["messages"][-1].content)
