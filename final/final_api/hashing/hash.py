import hashlib

import aioredis

from schemas import CreateUser

REDIS_URL = "redis://localhost:6380"


async def hash_and_save_password(password: str, user_id: int) -> None:
    redis = await aioredis.from_url(REDIS_URL)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    await redis.set(f"user:{user_id}:password", hashed_password)
    await redis.close()

    # GET user:8:password


async def add_user_to_redis(user: CreateUser, user_id: int) -> None:
    redis = await aioredis.from_url(REDIS_URL)
    user_data = user.dict()
    await redis.hmset(f"user:{user_id}", {key: str(value) for key, value in user_data.items()})
    await redis.close()

# Hash Redis: b7f3aa326111b20f7618601856afdfd911c67b4f338c7928eddd4fbb96cd4dba
