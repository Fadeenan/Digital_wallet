import pytest
from httpx import AsyncClient
from digimon import models

@pytest.mark.asyncio
async def test_create_wallet(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "user_id": token_user1.user_id,
        "balance": 100.0,
    }
    response = await client.post("/wallets", json=payload, headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data["balance"] == payload["balance"]
    assert data["user_id"] == payload["user_id"]

@pytest.mark.asyncio
async def test_read_wallet(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/wallets/1", headers=headers)  # Assuming wallet with ID 1 exists
    data = response.json()

    assert response.status_code == 200
    assert data["user_id"] == token_user1.user_id

@pytest.mark.asyncio
async def test_update_wallet(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "user_id": token_user1.user_id,
        "balance": 50.0,
    }
    response = await client.post("/wallets", json=payload, headers=headers)
    created_wallet = response.json()

    update_payload = {
        "balance": 150.0
    }
    response = await client.put(f"/wallets/{created_wallet['id']}", json=update_payload, headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data["balance"] == update_payload["balance"]

@pytest.mark.asyncio
async def test_delete_wallet(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "user_id": token_user1.user_id,
        "balance": 100.0,
    }
    response = await client.post("/wallets", json=payload, headers=headers)
    created_wallet = response.json()
    
    response = await client.delete(f"/wallets/{created_wallet['id']}", headers=headers)
    print(response.json())  # Print the response to inspect its content
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_wallet_not_found(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/wallets/9999", headers=headers)  # Assuming ID 9999 does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Wallet not found"
