import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound
from digimon import models


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": "password123"
    }
    response = await client.post("/users/create", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get(f"/users/{token_user1.user_id}", headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == token_user1.user_id
    assert data["username"] == "user1"


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    update_payload = {
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
        "email": "updateduser@example.com",
        "username": "updateduser"
    }
    response = await client.put(f"/users/{token_user1.user_id}/update", json=update_payload, headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data["first_name"] == update_payload["first_name"]
    assert data["last_name"] == update_payload["last_name"]
    assert data["email"] == update_payload["email"]
    assert data["username"] == update_payload["username"]


@pytest.mark.asyncio
async def test_change_password(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    password_payload = {
        "current_password": "123456",
        "new_password": "newpassword123"
    }
    response = await client.put(f"/users/{token_user1.user_id}/change_password", json=password_payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["detail"] == "Password updated successfully"


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, token_user1: models.Token, session: AsyncSession):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    
    response = await client.delete(f"/users/{token_user1.user_id}/delete", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted successfully"
    
    result = await session.exec(select(models.DBUser).where(models.DBUser.id == token_user1.user_id))
    user = result.first()

    assert user is None, "User was not deleted from the database"


@pytest.mark.asyncio
async def test_user_not_found(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/users/99999", headers=headers)  

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
