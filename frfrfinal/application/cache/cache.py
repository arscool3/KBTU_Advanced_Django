import json
from typing import Any

from fastapi.encoders import jsonable_encoder
from redis import Redis 

from application.db_app.settings import settings


class RedisRepository:

    def __init__(self):
        self.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

    def set_cache(self, name: str, value: Any, if_list: bool = False) -> bool | None:
        data = None
        if if_list is True:
            data = jsonable_encoder([i._mapping for i in value])
        if if_list is False:
            data = jsonable_encoder(value._mapping)
        serialized_data = json.dumps(data)
        return self.redis.set(name=name, value=serialized_data, ex=120)

    def get_cache(self, name: str) -> Any:
        cache = self.redis.get(name)
        if cache:
            return json.loads(cache)

    def delete_cache(self, name: str):
        if self.get_cache(name):
            return self.redis.delete(name)
