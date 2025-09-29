from confest import client

def test_health(client):
 r = client.get("/health")
 assert r.status_code == 200
 assert r.json() == {"status": "ok"}
