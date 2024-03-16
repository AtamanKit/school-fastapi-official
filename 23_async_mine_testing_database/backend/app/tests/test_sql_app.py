from httpx import AsyncClient
import pytest

from app.database import sessionmanager

import logging
import asyncio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    # logger.debug(f"Current event loop (user) before request: {id(asyncio.get_event_loop())}")
    response = await client.post(
        "/users/",
        json={"email": "bogdantitamir@example.com", "password": "chimichangas4life"},
    )
    # logger.debug(f"Current event loop (user) after request: {id(asyncio.get_event_loop())}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "bogdantitamir@example.com"
    assert "id" in data
    user_id = data["id"]

    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "bogdantitamir@example.com"
    assert data["id"] == user_id

    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 200, response.text


@pytest.mark.usefixtures("setup_database")
@pytest.mark.asyncio
async def test_create_item_user(client: AsyncClient):
    # logger.debug(f"Current event loop (item) before request: {id(asyncio.get_event_loop())}")
    response = await client.post("/users/", json={"email": "allapugachiova@example.com", "password": "secret"})
    data = response.json()
    user_id = data["id"]
    # logger.debug(f"Current event loop (item) after request: {id(asyncio.get_event_loop())}")

    response = await client.post(
        f"/users/{user_id}/items/",
        json={"title": "Million Alih Roz", "description": "A song by Alla Pugachiova"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Million Alih Roz"
    assert data["description"] == "A song by Alla Pugachiova"
    assert data["owner_id"] == user_id
    assert "id" in data
