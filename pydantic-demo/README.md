Documentation for version: v2.13.4.

Pydantic is the most widely used data validation library for Python.

Fast and extensible, Pydantic plays nicely with your linters/IDE/brain. Define how data should be in pure, canonical Python 3.9+; validate it with Pydantic.

#################################

Why use Pydantic?
Powered by type hints — with Pydantic, schema validation and serialization are controlled by type annotations; less to learn, less code to write, and integration with your IDE and static analysis tools. 
Speed — Pydantic’s core validation logic is written in Rust. As a result, Pydantic is among the fastest data validation libraries for Python. 
JSON Schema — Pydantic models can emit JSON Schema, allowing for easy integration with other tools. 
Strict and Lax mode — Pydantic can run in either strict mode (where data is not converted) or lax mode where Pydantic tries to coerce data to the correct type where appropriate. 
Dataclasses, TypedDicts and more — Pydantic supports validation of many standard library types including dataclass and TypedDict. 
Customisation — Pydantic allows custom validators and serializers to alter how data is processed in many powerful ways. 
Ecosystem — around 8,000 packages on PyPI use Pydantic, including massively popular libraries like FastAPI, huggingface, Django Ninja, SQLModel, & LangChain. 
Battle tested — Pydantic is downloaded over 550M times/month and is used by all FAANG companies and 20 of the 25 largest companies on NASDAQ. If you’re trying to do something with Pydantic, someone else has probably already done it. 

Installing Pydantic is as simple as: pip install pydantic