import time
import random

__all__ = ["get_person_traffic_data"]


def get_person_traffic_data() -> dict:
    return {
        "person_id": random.randint(1, 1),
        "traffic_data": {
            "timestamp": time.time(),
            "location": {
                "latitude": round(random.uniform(1, 30), 5),
                "longitude": round(random.uniform(1, 40), 5),
            },
            "speed": random.randint(0, 100),
            "acceleration": round(random.uniform(0, 100), 3),
            "direction": random.randint(0, 360),
        },
    }
