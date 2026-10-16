import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Copy .env.example to .env in this folder and add your key."
    )

# from langchain.tools import tool
# from langchain.agents import create_agent
# from langchain.chat_models import init_chat_model

# model = init_chat_model("openai:gpt-5-mini")
# print("Model ready.")

# Pattern 4: Router -- minimal example.
# A classification step fans out to agents in parallel, then a synthesis step combines results.
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

class RouterState(TypedDict, total=False):
    query: str
    answers: Annotated[list[str], operator.add]
    final: str

def classify(query: str) -> list[str]:
    targets = []
    if "showtime" in query.lower() or "time" in query.lower():
        targets.append("showtimes")
    if "refund" in query.lower():
        targets.append("policy")
    return targets or ["showtimes"]

def route(state: RouterState):
    return [Send(t, {"query": state["query"]}) for t in classify(state["query"])]

def showtimes_node(state) -> dict:
    return {"answers": ["Interstellar: 7:00 PM and 10:15 PM."]}

def policy_node(state) -> dict:
    return {"answers": ["Refunds available up to 2 hours before showtime."]}

def synthesize(state: RouterState) -> dict:
    return {"final": " | ".join(state["answers"])}

router_graph = (
    StateGraph(RouterState)
    .add_node("showtimes", showtimes_node)
    .add_node("policy", policy_node)
    .add_node("synthesize", synthesize)
    .add_conditional_edges(START, route, ["showtimes", "policy"])
    .add_edge("showtimes", "synthesize")
    .add_edge("policy", "synthesize")
    .add_edge("synthesize", END)
    .compile()
)

# result = router_graph.invoke({"query": "What time does it show and can I get a refund?"})
# print(result["final"])
# Interstellar: 7:00 PM and 10:15 PM. | Refunds available up to 2 hours before showtime.