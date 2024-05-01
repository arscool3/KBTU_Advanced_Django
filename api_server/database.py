import confluent_kafka
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

url = "postgresql://postgres:password@postgres/postgres"

engine = create_engine(url)


def get_db():
    try:
        session = Session(engine)
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


def get_kafka_producer():
    producer = confluent_kafka.Producer(
        {
            "bootstrap.servers": "localhost:9092"
        }
    )
    yield producer
    producer.commit_transaction()