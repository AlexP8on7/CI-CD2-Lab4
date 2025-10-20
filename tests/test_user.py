# tests/test_users.py

import pytest
import uuid

def user_payload(name="Alex", email=None, age=25, sid=None):
    if email is None:
        email = f"test{uuid.uuid4().hex[:8]}@atu.ie"
    if sid is None:
        import random
        sid = f"S{random.randint(1000000, 9999999)}"
    return {"name": name, "email": email, "age": age, "student_id": sid}

def test_create_user_ok(client):
    """tests if you can successfully create a user"""
    result = client.post("/api/users", json=user_payload())
    assert result.status_code == 201
    data = result.json()
    assert "id" in data
    assert data["name"] == "Alex"

def test_duplicate_user_id_conflict(client):
    """tests you can create a user with an existing id"""
    payload = user_payload()
    client.post("/api/users", json=payload)
    result = client.post("/api/users", json=payload)
    assert result.status_code == 409 # duplicate id -> conflict
    assert "exists" in result.json()["detail"].lower()

@pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])
def test_bad_student_id_422(client, bad_sid):
    """tests invalid user ids throw 422 error"""
    result = client.post("/api/users", json=user_payload(sid=bad_sid))
    assert result.status_code == 422 # pydantic validation error

def test_get_user_404(client):
    """tests 404 is thrown when a user does not exist when trying to get them"""
    result = client.get("/api/users/999")
    assert result.status_code == 404

def test_delete_then_404(client):
    """tests 404 is throw when trying to delete a user who does not exist"""
    result = client.post("/api/users", json=user_payload())
    user_id = result.json()["id"]
    result1 = client.delete(f"/api/delete/users/{user_id}")
    assert result1.status_code == 204
    result2 = client.delete(f"/api/delete/users/{user_id}")
    assert result2.status_code == 404

def test_edit_user_ok(client):
    """tests you can edit an existing user"""
    payload = user_payload()
    result = client.post("/api/users", json=payload)
    user_id = result.json()["id"]
    result1 = client.put(f"/api/users/{user_id}", json=user_payload(email=payload["email"], sid=payload["student_id"], age=20))
    assert result1.status_code == 200

def test_edit_user_404(client):
    """tests you can't edit a user that does not exist"""
    client.post("/api/users", json=user_payload())
    result = client.put("/api/users/999", json=user_payload(age=20))
    assert result.status_code == 404

@pytest.mark.parametrize("bad_age", ["BAD", "10", "$^", "bad"])
def test_bad_age_422(client, bad_age):
    """tests invalid ages"""
    result = client.post("/api/users", json=user_payload(age=bad_age))
    assert result.status_code == 422 # pydantic validation error