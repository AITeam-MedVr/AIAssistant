from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_upload_data():
    response = client.post("/upload/data", json={ "object_id": "123", "session_id": "abc", "data": [] })
    assert response.status_code == 403  # No API key provided
