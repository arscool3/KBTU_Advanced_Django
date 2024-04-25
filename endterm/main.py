from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.api import api_router
from db.session import engine
from db.base import Base
from app.dependencies import get_db
from kfka.producer import KafkaProducerWrapper

app = FastAPI(title="E-commerce Order System")

app.include_router(api_router)

# kafka_producer = KafkaProducerWrapper(servers="localhost:9092")

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():
    print("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    # kafka_producer.close()

@app.get("/")
async def root():
    return {"message": "Hello World from your E-commerce Order System"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
