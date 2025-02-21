from fastapi import APIRouter, Depends, Header, HTTPException
from server.app.services.auth import redis_client
from server.app.services.auth import store_api_key, verify_api_key
from server.app.core.config import MASTER_API_KEY
from server.app.services.storage import save_data, get_data, clear_storage, export_storage

from server.app.services.rate_limit import check_rate_limit


router = APIRouter()

@router.get("/test-redis")
def test_redis():
    redis_client.set("foo", "bar")
    value = redis_client.get("foo")
    return {"message": f"Redis is working! Value: {value}"}


@router.post("/store-api-key")
def add_api_key(
    api_key: str,
    client_id: str,
    rate_limit: int = 60,
    master_key: str = Header(None, alias="X-Master-Key")  # Secure API Key Creation
):
    """
    Securely store an API key in Redis, only if the master API key is provided.
    """
    if master_key != MASTER_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid Master API Key")
    else:
        store_api_key(api_key, client_id, rate_limit)
    return {"message": "API Key stored successfully"}

@router.get("/secure-data")
def secure_endpoint(api_key: str = Header(None, alias="X-API-Key")):
    """
    Protected endpoint that requires an API key and enforces rate limits.
    """
    if not api_key:
        raise HTTPException(status_code=403, detail="API Key missing")

    client_id = verify_api_key(api_key)
    check_rate_limit(api_key)

    return {"message": f"Hello, {client_id}! You are authorized."}


@router.post("/store-data")
def store_data(key: str, data: dict):
    """API to store data in JSON storage."""
    return save_data(key, data)

@router.get("/get-data")
def fetch_data(key: str):
    """API to retrieve stored data."""
    result = get_data(key)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.delete("/clear-storage")
def clear_all_data():
    """API to clear the storage."""
    return clear_storage()

@router.get("/export-storage")
def export_all_data():
    """API to export the entire storage as JSON."""
    return export_storage()