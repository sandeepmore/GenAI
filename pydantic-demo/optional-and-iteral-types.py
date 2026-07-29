# Reference: https://pydantic-with-mayank.netlify.app/
# Two more type-hint patterns show up constantly once Pydantic enters the picture — and become especially important later when constraining what an AI model is allowed to return.

# Optional (or the modern | None syntax) marks a value that might legitimately not exist yet: phone: str | None = None. Both Optional[str] and str | None mean exactly the same thing; the pipe syntax is preferred in modern Python (3.10+).

# Literal restricts a value to an exact, specific set of options — a multiple-choice question instead of a fill-in-the-blank: status: Literal["draft", "published", "archived"]. On its own (still without Pydantic), this is only documentation. Once Pydantic enforces it, Literal becomes a genuinely powerful tool — especially for constraining AI-generated classifications, covered in depth later.

from typing import Optional, Literal

# Optional — old style and modern style mean the same thing
middle_name: Optional[str] = None
phone: str | None = None

# Literal — a strict multiple-choice constraint
status: Literal["draft", "published", "archived"] = "draft"
priority: Literal["low", "medium", "high"] = "medium"

# Still just documentation at this stage — Python allows this:
status = "this is not one of the allowed options"  # no error yet