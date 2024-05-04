# Lecture 10 | Binance? project

## HOW TO RUN

-
    1) docker-compose up
-
    2) alembic upgrade head
-
    3) python producer/producer.py | to run producer
-
    4) uvicorn c_server.py --reload --port 8001 | to run consumer server
-
    5) python i_script.py | to run insurance script
-
    6) uvicorn main_app:app --reload
-
    7) to see a heatmap go to http://127.0.0.1:8000/data/heatmap/