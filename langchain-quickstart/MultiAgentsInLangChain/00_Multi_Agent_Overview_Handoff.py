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

# Pattern 2: Handoffs -- minimal example.
# A single agent's prompt and tools change based on a state field, via middleware.
from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing_extensions import NotRequired
from typing import Literal, Callable

class TicketState(AgentState):
    stage: NotRequired[Literal["greeting", "booking"]]

@wrap_model_call
def apply_stage(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    stage = request.state.get("stage", "greeting")
    if stage == "greeting":
        request = request.override(system_prompt="Greet the customer and ask what movie they want.")
    else:
        request = request.override(system_prompt="Help the customer pick a showtime and confirm the booking.")
    return handler(request)

handoff_agent = create_agent(model, tools=[], middleware=[apply_stage], state_schema=TicketState)
result = handoff_agent.invoke({"messages": [{"role": "user", "content": "Hi"}], "stage": "greeting"})
print(result["messages"][-1].content)