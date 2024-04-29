import os

__all__ = ["JWT_SECRET", "DATABASE_URL"]

JWT_SECRET = os.environ.get("JWT_SECRET")
DATABASE_URL = os.environ.get("DATABASE_URL")
