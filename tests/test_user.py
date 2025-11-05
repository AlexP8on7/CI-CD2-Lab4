import pytest
import uuid

def user_payload(name="Alex", email=None, age=25, sid=None):
    if email is None:
        email = f"test{uuid.uuid4().hex[:8]}@atu.ie"
    if sid is None:
        import random
        sid = f"S{random.randint(1000000, 9999999)}"
    return {"name": name, "email": email, "age": age, "student_id": sid}

def project_payload(name="Test Project", description="Test Description", owner_id=1):
    return {"name": name, "description": description, "owner_id": owner_id}

# User Tests
def test_create_user_ok(client):
    """tests if you can successfully create a user"""
    result = client.post("/api/users", json=user_payload())
    assert result.status_code == 201
    data = result.json()
    assert "id" in data
    assert data["name"] == "Alex"

def test_user_put_full_update(client):
    """Test PUT endpoint for full user update"""
    # Create user
    user_data = user_payload()
    result = client.post("/api/users", json=user_data)
    user_id = result.json()["id"]
    
    # Update user with PUT
    updated_data = user_payload(name="Updated Name", age=30, email=user_data["email"], sid=user_data["student_id"])
    result = client.put(f"/api/users/{user_id}", json=updated_data)
    assert result.status_code == 200
    data = result.json()
    assert data["name"] == "Updated Name"
    assert data["age"] == 30

def test_user_patch_partial_update(client):
    """Test PATCH endpoint for partial user update"""
    # Create user
    user_data = user_payload()
    result = client.post("/api/users", json=user_data)
    user_id = result.json()["id"]
    
    # Partial update with PATCH
    patch_data = {"name": "Patched Name"}
    result = client.patch(f"/api/users/{user_id}", json=patch_data)
    assert result.status_code == 200
    data = result.json()
    assert data["name"] == "Patched Name"
    assert data["age"] == user_data["age"]  # Should remain unchanged

# Project Tests
def test_project_put_full_update(client):
    """Test PUT endpoint for full project update"""
    # Create user first
    user_result = client.post("/api/users", json=user_payload())
    user_id = user_result.json()["id"]
    
    # Create project
    project_data = project_payload(owner_id=user_id)
    result = client.post("/api/projects", json=project_data)
    project_id = result.json()["id"]
    
    # Update project with PUT
    updated_data = project_payload(name="Updated Project", description="Updated Description", owner_id=user_id)
    result = client.put(f"/api/projects/{project_id}", json=updated_data)
    assert result.status_code == 200
    data = result.json()
    assert data["name"] == "Updated Project"
    assert data["description"] == "Updated Description"

def test_project_patch_partial_update(client):
    """Test PATCH endpoint for partial project update"""
    # Create user first
    user_result = client.post("/api/users", json=user_payload())
    user_id = user_result.json()["id"]
    
    # Create project
    project_data = project_payload(owner_id=user_id)
    result = client.post("/api/projects", json=project_data)
    project_id = result.json()["id"]
    
    # Partial update with PATCH
    patch_data = {"name": "Patched Project"}
    result = client.patch(f"/api/projects/{project_id}", json=patch_data)
    assert result.status_code == 200
    data = result.json()
    assert data["name"] == "Patched Project"
    assert data["description"] == project_data["description"]  # Should remain unchanged

def test_duplicate_user_id_conflict(client):
    """tests you can create a user with an existing id"""
    payload = user_payload()
    client.post("/api/users", json=payload)
    result = client.post("/api/users", json=payload)
    assert result.status_code == 409
    assert "exists" in result.json()["detail"].lower()

@pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])
def test_bad_student_id_422(client, bad_sid):
    """tests invalid user ids throw 422 error"""
    result = client.post("/api/users", json=user_payload(sid=bad_sid))
    assert result.status_code == 422

def test_get_user_404(client):
    """tests 404 is thrown when a user does not exist when trying to get them"""
    result = client.get("/api/users/999")
    assert result.status_code == 404

def test_delete_then_404(client):
    """tests 404 is throw when trying to delete a user who does not exist"""
    result = client.post("/api/users", json=user_payload())
    user_id = result.json()["id"]
    result1 = client.delete(f"/api/users/{user_id}")
    assert result1.status_code == 204
    result2 = client.delete(f"/api/users/{user_id}")
    assert result2.status_code == 404

def test_edit_user_404(client):
    """tests you can't edit a user that does not exist"""
    result = client.put("/api/users/999", json=user_payload())
    assert result.status_code == 404