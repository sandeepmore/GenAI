# Reference: https://pydantic-with-mayank.netlify.app/
# Type hints: documentation, not enforcement
# Type hints are the foundation everything else in this guide is built on. They tell Python — and every developer reading the code — what type a variable is *supposed* to hold: name: str, age: int, price: float, is_active: bool.

# Here's the part that trips people up: Python does not enforce type hints at runtime. This line runs without a single complaint: age: int = "not a number at all". Type hints are read by humans, by your IDE (for autocomplete and error squiggles), and — critically — by Pydantic. But plain Python itself ignores them completely.

# Container types follow the same pattern: list[str] for a list of strings, dict[str, int] for a dictionary mapping strings to integers. Since Python 3.9+, use these lowercase built-ins directly rather than importing List/Dict from typing — you'll still see the older style in existing codebases, but the lowercase form is the modern standard.

# The four basic types you'll use constantly
name: str = "Aditi"
age: int = 28
price: float = 499.99
is_active: bool = True

# Container types
tags: list[str] = ["python", "pydantic", "fastapi"]
word_counts: dict[str, int] = {"error": 12, "warning": 5}

# Function signatures — the most valuable place to use hints
def format_price(amount: float, currency: str = "USD") -> str:
    return f"{currency} {amount:.2f}"

# The gotcha: Python enforces NONE of this
age: int = "not a number at all"   # runs. no error. no warning.

print(f"Age is {age}, but Python doesn't care that it's not an int. Type hints are just documentation, not enforcement.")