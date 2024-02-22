from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={"email": "alapugachova@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "alapugachova@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "alapugachova@example.com"
    assert data["id"] == user_id
