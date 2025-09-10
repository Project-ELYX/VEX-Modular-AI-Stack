import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_config_roundtrip():
    resp = client.post(
        "/api/config",
        json={
            "openrouter_api_key": "test-key",
            "anthropic_api_key": "ant-key",
            "mode": "remote",
        },
        headers={"X-Token": "secret-token"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["openrouter_api_key"] == "test-key"
    resp = client.get("/api/config", headers={"X-Token": "secret-token"})
    assert resp.json()["mode"] == "remote"
