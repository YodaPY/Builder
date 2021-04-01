import os
from typing import Final
from dotenv import load_dotenv

__all__ = (
    "POSTGRES_DATABASE", "POSTGRES_PASSWORD",
    "POSTGRES_USER", "POSTGRES_HOST",
    "TOKEN"
)

load_dotenv()

POSTGRES_DATABASE: Final[str] = os.environ.get("POSTGRES_DATABASE") or "Builder"
POSTGRES_PASSWORD: Final[str] = os.environ["POSTGRES_PASSWORD"]
POSTGRES_USER: Final[str] = os.environ.get("POSTGRES_USER") or "postgres"
POSTGRES_HOST: Final[str] = os.environ.get("POSTGRES_HOST") or None
TOKEN: Final[str] = os.environ["TOKEN"]
DEFAULT_PREFIX: Final[str] = "b!"