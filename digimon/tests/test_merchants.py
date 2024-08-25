import pytest
from httpx import AsyncClient
from digimon import models

@pytest.mark.asyncio
async def test_create_merchant(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "name": "Test Merchant",
        "description": "A test merchant",
        "tax_id": "1234567890",
        "user_id": token_user1.user_id,
    }
    response = await client.post("/merchants", json=payload, headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == payload["name"]
    assert data["id"] > 0

@pytest.mark.asyncio
async def test_read_merchants(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/merchants", headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data["merchants"], list)
    assert len(data["merchants"]) > 0

@pytest.mark.asyncio
async def test_read_merchant_by_id(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/merchants/1", headers=headers)  # Assuming merchant with ID 1 exists
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == 1

@pytest.mark.asyncio
async def test_update_merchant(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "name": "Test Merchant",
        "description": "A test merchant",
        "tax_id": "1234567890",
        "user_id": token_user1.user_id,
    }
    response = await client.post("/merchants", json=payload, headers=headers)
    created_merchant = response.json()

    update_payload = {
        "name": "Updated Merchant Name",
        "description": "Updated description",
        "tax_id": created_merchant['tax_id'],
        "user_id": created_merchant['user_id']
    }
    response = await client.put(f"/merchants/{created_merchant['id']}", json=update_payload, headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == update_payload["name"]

@pytest.mark.asyncio
async def test_delete_merchant(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "name": "Test Merchant",
        "description": "A test merchant",
        "tax_id": "1234567890",
        "user_id": token_user1.user_id,
    }
    response = await client.post("/merchants", json=payload, headers=headers)
    created_merchant = response.json()

    response = await client.delete(f"/merchants/{created_merchant['id']}", headers=headers)
    assert response.status_code == 200
    assert "delete success" in response.json()["message"]

@pytest.mark.asyncio
async def test_merchant_not_found(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/merchants/9999", headers=headers)  
    assert response.status_code == 404
    assert response.json()["detail"] == "Merchant not found"
