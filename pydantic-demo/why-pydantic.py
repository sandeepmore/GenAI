# Reference: https://pydantic-with-mayank.netlify.app/
# Why Pydantic Exists
# Python won't stop you from shipping garbage data. Pydantic is the fix — but first, the foundation it's built on: type hints.

# The dynamic typing problem
# Python is dynamically typed. A single variable can hold an integer, then a string, then a list, with zero complaints from the language itself. This flexibility is genuinely useful for quick scripts — and genuinely dangerous the moment you're working with data that came from *outside* your own code: an API response, a form submission, a file upload, or an LLM.

# Consider a typical register_user() function that receives a dictionary and calculates a birth year from an age field. It looks completely reasonable. It works perfectly — right up until age arrives as the string "unknown" instead of a number, at which point the program crashes deep inside a calculation, often several function calls away from where the bad data actually entered the system.

# The bug was never really in the calculation. The bug was that nothing checked the incoming data at the door.

def register_user(name, email, age):
    birth_year = 2026 - age   # assumes age is an int — nothing enforces that
    print(f"Registered {name}, born approx. {birth_year}")

# Looks fine...
register_user("Aditi", "aditi@example.com", 28)

# ...until real-world data shows up like this:
register_user("Rohan", "rohan@example.com", "unknown")
# TypeError: unsupported operand type(s) for -: 'int' and 'str'
# Notice WHERE it crashed: deep inside the function, not at the door.

