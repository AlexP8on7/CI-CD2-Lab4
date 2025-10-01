#test_health.py
import pytest

#health test
def test_health(client):
    result = client.get("/health")
    assert result.status_code == 200
    assert result.json() == {"status": "ok"}