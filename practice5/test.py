import pytest

from fastapi.testclient import TestClient
from main import app

from database import Base

client = TestClient(app)

