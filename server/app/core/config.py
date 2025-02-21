import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "tolerant-skunk-17796.upstash.io")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "AUWEAAIjcDE4NTczOWNiNmYzZjI0OTE0YTdlMmVlZjAzMjc3NTE0ZXAxMA")
REDIS_SSL = os.getenv("REDIS_SSL", "True") == "True"  # Ensure boolean conversion
MASTER_API_KEY = os.getenv("MASTER_API_KEY", "supersecretmasterkey")  # Hardcoded security key