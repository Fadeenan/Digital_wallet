

import pytest
from httpx import AsyncClient
from digimon import models

@pytest.mark.asyncio
async def test_create_transaction(client: AsyncClient, token_user1: models.Token, session: models.AsyncSession):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    
    wallet_payload = {"user_id": token_user1.user_id, "balance": 100.0}
    wallet = models.DBWallet(**wallet_payload)
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)
    
    transaction_payload = {
        "wallet_id": wallet.id,
        "amount": 50.0,
        "type": "debit",
        "description": "Test transaction"
    }
    response = await client.post("/transactions", json=transaction_payload, headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data["amount"] == transaction_payload["amount"]
    assert data["description"] == transaction_payload["description"]
    assert data["type"] == transaction_payload["type"]

@pytest.mark.asyncio
async def test_read_transaction(client: AsyncClient, token_user1: models.Token, session: models.AsyncSession):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    
    wallet_payload = {"user_id": token_user1.user_id, "balance": 100.0}
    wallet = models.DBWallet(**wallet_payload)
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)
    
    transaction_payload = {
        "wallet_id": wallet.id,
        "amount": 50.0,
        "type": "debit",
        "description": "Test transaction"
    }
    response = await client.post("/transactions", json=transaction_payload, headers=headers)
    created_transaction = response.json()

    response = await client.get(f"/transactions/{created_transaction['id']}", headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data["amount"] == created_transaction["amount"]
    assert data["description"] == created_transaction["description"]

@pytest.mark.asyncio
async def test_update_transaction(client: AsyncClient, token_user1: models.Token, session: models.AsyncSession):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    
    # Create a wallet and transaction for testing
    wallet_payload = {"user_id": token_user1.user_id, "balance": 100.0}
    wallet = models.DBWallet(**wallet_payload)
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)
    
    transaction_payload = {
        "wallet_id": wallet.id,
        "amount": 50.0,
        "type": "debit",
        "description": "Initial transaction"
    }
    response = await client.post("/transactions", json=transaction_payload, headers=headers)
    created_transaction = response.json()

    # Update the transaction
    update_payload = {
        "wallet_id": wallet.id,  # Include wallet_id to ensure schema validation
        "amount": 75.0,
        "type": "debit",
        "description": "Updated transaction"
    }
    response = await client.put(f"/transactions/{created_transaction['id']}", json=update_payload, headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data["amount"] == update_payload["amount"]
    assert data["description"] == update_payload["description"]

@pytest.mark.asyncio
async def test_update_transaction_insufficient_funds(client: AsyncClient, token_user1: models.Token, session: models.AsyncSession):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    
    # Create a wallet with insufficient balance for the update
    wallet_payload = {"user_id": token_user1.user_id, "balance": 50.0}
    wallet = models.DBWallet(**wallet_payload)
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)
    
    # Create a transaction
    transaction_payload = {
        "wallet_id": wallet.id,
        "amount": 40.0,
        "type": "debit",
        "description": "Initial transaction"
    }
    response = await client.post("/transactions", json=transaction_payload, headers=headers)
    created_transaction = response.json()

    # Attempt to update the transaction with an amount greater than the wallet balance
    update_payload = {
        "wallet_id": wallet.id,  # Include wallet_id to ensure schema validation
        "amount": 60.0,  # Exceeds remaining balance
        "type": "debit",
        "description": "Updated transaction"
    }
    response = await client.put(f"/transactions/{created_transaction['id']}", json=update_payload, headers=headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient funds"

@pytest.mark.asyncio
async def test_delete_transaction(client: AsyncClient, token_user1: models.Token, session: models.AsyncSession):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    
    wallet_payload = {"user_id": token_user1.user_id, "balance": 100.0}
    wallet = models.DBWallet(**wallet_payload)
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)
    
    transaction_payload = {
        "wallet_id": wallet.id,
        "amount": 50.0,
        "type": "debit",
        "description": "Test transaction"
    }
    response = await client.post("/transactions", json=transaction_payload, headers=headers)
    created_transaction = response.json()

    response = await client.delete(f"/transactions/{created_transaction['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction deleted successfully"

    response = await client.get(f"/transactions/{created_transaction['id']}", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction not found"

@pytest.mark.asyncio
async def test_delete_transaction_not_found(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}

    response = await client.delete("/transactions/9999", headers=headers)  
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction not found"
