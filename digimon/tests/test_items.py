import pytest
from httpx import AsyncClient
from digimon import models


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "merchant_id": 1,
    }
    response = await client.post("/items", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == payload["name"]
    assert data["id"] > 0


@pytest.mark.asyncio
async def test_read_items(client: AsyncClient):
    response = await client.get("/items?page=1")
    data = response.json()

    assert response.status_code == 200
    assert len(data["items"]) >= 1


@pytest.mark.asyncio
async def test_read_item(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "merchant_id": 1,
    }
    response = await client.post("/items", json=payload, headers=headers)

    created_item = response.json()

    response = await client.get(f"/items/{created_item['id']}", headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == created_item["name"]


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "merchant_id": 1,
    }
    response = await client.post("/items", json=payload, headers=headers)
    created_item = response.json()

    # Ensure the update payload includes all necessary fields
    update_payload = {
        "name": "Updated Item Name",
        "description": "Updated description",
        "price": 12.99,
        "merchant_id": created_item['merchant_id']  # Ensure merchant_id is included
    }
    response = await client.put(f"/items/{created_item['id']}", json=update_payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == update_payload["name"]


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "merchant_id": 1,
    }
    response = await client.post("/items", json=payload, headers=headers)
    created_item = response.json()

    response = await client.delete(f"/items/{created_item['id']}", headers=headers)

    assert response.status_code == 200
    assert "delete success" in response.json()["message"]
