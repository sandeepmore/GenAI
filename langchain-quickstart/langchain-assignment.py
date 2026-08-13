# Your capstone solution
from pydantic import BaseModel, Field
from typing import Literal, Union
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_core.messages import AIMessage

from langchain_core.tools import tool
from langchain.tools import ToolRuntime
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable
from dataclasses import dataclass
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.agents.middleware import ToolCallLimitMiddleware

from rich import print

loyalty_store = InMemoryStore()

@dataclass
class customerContext:
    customer_id: str
    customer_location: str


################ Strctured Schemas ###########################
class greenPlateNewReservation(BaseModel):
  customer_name: str = Field(description="Name of the customer")
  party_size: int = Field(ge=1, le=20, description="Number of person")
  time_slot: str = Field(description="Time slot for reservation")

class greenPlateCancelReservation(BaseModel):
  customer_name: str = Field(description="Name of the customer")
  time_slot: str = Field(description="Time slot for reservation")

class greenPlateFoodOrder(BaseModel):
  customer_name: str = Field(description="Name of the customer")
  dish_name: str = Field(description="Name of the dish")
  quantity: int = Field(ge=1, le=10, description="Quantity of the Dish")
  spice_level: Literal["mild", "medium", "hot"] = Field(description="Spice level of the dish")

################ Strctured Schemas END ###########################

################ Custom Tools ###########################
@tool("StandardDiningRoomBooking", description="For standard booking and non-premium members only")
def book_standard_dining_room(customer_name: str, no_of_seats: int, return_direct=True) -> str:
  """Book a standard dining room. No further questions."""
  return f"Standard dining room is booked with name - {customer_name}."

@tool("PrivateDiningRoomBooking", description="For private booking and premium members only")
def book_private_dining_room(customer_name: str, no_of_seats: int, return_direct=True) -> str:
  """Book a Private dining room, for premium membership only. No further questions."""
  return f"Private dining room is booked with name - {customer_name}."

@tool
def save_dietary_preference(customer_id: str, preference: str, runtime: ToolRuntime) -> str:
  """Saves customers Dietary preference"""
  runtime.store.put(
    (customer_id, "preferences"),     # namespace
    "dietary_preference",             # key
    {"value": preference}             # value
  )
  return f"Got it, I will remember, you like {preference}"

@tool
def recall_dietary_preference(customer_id: str, runtime: ToolRuntime) -> str:
  """Recall customers Dietary preference"""
  preference = runtime.store.get(
    (customer_id, "preferences"),
    "dietary_preference"
  )
  return f"You like {preference}"

################ Custom Tools END ###########################

################ Dynamic Tool Gating - Premium member ###########################
@wrap_model_call
def gate_private_tools(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    """Only expose book_private_dining_room to premium members."""
    is_premium = request.state.get("is_premium_member", False)
    if not is_premium:
        allowed = [t for t in request.tools if t.name != "book_private_dining_room"]
        request = request.override(tools=allowed)
    return handler(request)

################ Dynamic Tool Gating - END ###########################

greenPlateAgent = create_agent(
    model="openai:gpt-5-mini",
    response_format=ToolStrategy(Union[greenPlateNewReservation, greenPlateCancelReservation, greenPlateFoodOrder]),
    tools=[book_standard_dining_room, book_private_dining_room, save_dietary_preference, recall_dietary_preference],
    # middleware=[gate_private_tools],
    store=loyalty_store,
    middleware=[
        gate_private_tools,
        ModelCallLimitMiddleware(
            thread_limit=10,
            run_limit=5,
            exit_behavior="end",
        ),
        # Global limit
        ToolCallLimitMiddleware(
            thread_limit=5,
            run_limit=5,
        ),
    ],
)

##### User Request1
response1 = greenPlateAgent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Hi, I'm Sandeep, please remember I am pure Vegiterian. I would like to order 2 medium spice butter paneer please."
            }
        ],
       "is_premium_member": False
    },
    config={
        "configurable": {
            "thread_id": "greenplate_thread_001"
        }
    },
    context=customerContext(
        customer_id="sandeep_001",
        customer_location="Mumbai"
    ),
)
print('#'*100)
print(response1)

response2 = greenPlateAgent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Hi, I'm Sandeep, would like book private dining room please."
            }
        ],
       "is_premium_member": False
    },
    config={
        "configurable": {
            "thread_id": "greenplate_thread_001"
        }
    },
    context=customerContext(
        customer_id="sandeep_001",
        customer_location="Mumbai"
    ),
)
print('#'*100)
print(response2)

# response3 = greenPlateAgent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "Hi, I'm Sandeep, please remember I am pure Vegiterian. I would like book standard dining room. And I would like to order 2 medium spice butter paneer please."
#             }
#         ],
#          "is_premium_member": False
#     },
#     config={
#         "configurable": {
#             "thread_id": "greenplate_thread_001"
#         }
#     },
#     context=customerContext(
#         customer_id="sandeep_001",
#         customer_location="Mumbai"
#     ),
# )
# print('#'*100)
# print(response3)

response4 = greenPlateAgent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Hi, I'm Rahul, please remember I am Non Vegiterian. I would like book private dining room. And I would like to order 2 spicy butter chicken masala please."
            }
        ],
        "is_premium_member": False
    },
    config={
        "configurable": {
            "thread_id": "greenplate_thread_002"
        }
    },
    context=customerContext(
        customer_id="Rahul_001",
        customer_location="Delhi"
    ),
)
print('#'*100)
print(response4)