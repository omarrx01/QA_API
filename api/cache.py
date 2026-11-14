
import os
import redis

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

CACHE_TTL = 3600  # 1 hour

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2
)


def get_cached_answer(question: str):
    try:
        return redis_client.get(f"qa:{question}")
    except redis.RedisError:
        return None


def cache_answer(question: str, answer: str):
    try:
        redis_client.setex(
            f"qa:{question}",
            CACHE_TTL,
            answer
        )
    except redis.RedisError:
        pass
