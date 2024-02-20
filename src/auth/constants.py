from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"


class InactiveDetail:
    DETAIL = "Inactive User"


class InvalidUserOrPassDetail:
    DETAIL = "Invalid Username or Password"
