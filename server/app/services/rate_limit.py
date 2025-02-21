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

def check_rate_limit(api_key: str):
    """
    Enforce rate limiting for API keys.
    """
    rate_limit = redis_client.get(f"rate_limit:{api_key}")
    if not rate_limit:
        rate_limit = 60  # Default to 60 requests per minute if not set

    key = f"rate_limit_count:{api_key}"
    request_count = redis_client.get(key)

    if request_count and int(request_count) >= int(rate_limit):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Increment request count and set expiration to 60 seconds
    redis_client.incr(key)
    redis_client.expire(key, 60)