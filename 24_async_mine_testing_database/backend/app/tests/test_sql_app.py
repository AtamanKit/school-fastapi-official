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

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200, response.text

def test_create_item_user(client):
    response = client.post("/users/", json={"email": "allapugachiova@example.com", "password": "secret"})
    data = response.json()
    user_id = data["id"]

    response = client.post(
        f"/users/{user_id}/items/",
        json={"title": "Million Alih Roz", "description": "A song by Alla Pugachiova"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Million Alih Roz"
    assert data["description"] == "A song by Alla Pugachiova"
    assert data["owner_id"] == user_id
    assert "id" in data
    
    