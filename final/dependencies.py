from fastapi import Depends
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def log_request():
    print("Logging request...")
    print("✓")
class RequestCounter:
    def __init__(self):
        self.counter = 0

    def __call__(self):
        self.counter += 1
        print(f"Total requests processed: {self.counter}")
