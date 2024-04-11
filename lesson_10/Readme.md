# Lecture 10 | Binance? project

## HOW TO RUN

- 1) docker-compose up
- 2) alembic upgrade head
- 3) python core/producer.py | to run producer
- 4) python core/consumer.py | to run consumer
- 5) uvicorn fastapi_app:app --reload | inside /core/
- 6) to see a heatmap go to http://127.0.0.1:8000/data/heatmap/