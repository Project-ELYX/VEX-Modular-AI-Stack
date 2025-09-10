import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from backend.main import app


def test_root_endpoint():
    client = TestClient(app)
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json() == {'status': 'ok'}
