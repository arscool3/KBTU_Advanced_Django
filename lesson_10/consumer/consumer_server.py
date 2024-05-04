from fastapi import FastAPI, Response
from .consumer import consume
from threading import Thread, active_count

app = FastAPI(name="CONSUMER")

consumer_thread = Thread(target=consume)
consumer_thread.start()


@app.get("/health-check/")
def health_check():
    global consumer_thread
    print("\n\n\n\n\n\n", active_count(), "\n\n\n\n\n\n")
    if consumer_thread.is_alive():
        return {"message": "Ok"}
    else:
        consumer_thread = Thread(target=consume)
        consumer_thread.start()
        return Response(status_code=500)
