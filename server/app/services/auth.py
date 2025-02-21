import redis
from fastapi import HTTPException
from server.app.core.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_SSL

# Connect to Upstash Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=REDIS_SSL,
    decode_responses=True  # Ensures string output
)

def store_api_key(api_key: str, client_id: str, rate_limit: int):
    """
    Store API key in Redis with the associated client ID and rate limit.
    """
    redis_client.set(f"api_key:{api_key}", client_id)
    redis_client.set(f"rate_limit:{api_key}", rate_limit)

def verify_api_key(api_key: str):
    """
    Verify if the API key exists in Redis.
    """
    if not api_key:
        raise HTTPException(status_code=403, detail="API Key missing")

    client_id = redis_client.get(f"api_key:{api_key}")

    if not client_id:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return client_id