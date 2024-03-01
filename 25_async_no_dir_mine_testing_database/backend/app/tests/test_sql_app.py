def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "bogdantitamir@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "bogdantitamir@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "bogdantitamir@example.com"
    assert data["id"] == user_id
