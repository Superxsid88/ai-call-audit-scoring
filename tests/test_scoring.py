from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_score_endpoint():
    payload = {
        "call_id": "t1",
        "transcript": "Hello, welcome to support. May I put you on hold? Thanks for waiting, issue resolved.",
        "lang": "en"
    }
    r = client.post("/score", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "scores" in data and "audit_meta" in data
