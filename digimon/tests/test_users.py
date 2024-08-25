# import pytest
# from httpx import AsyncClient
# from digimon import models

# @pytest.mark.asyncio
# async def test_create_user(client: AsyncClient):
#     payload = {
#         "username": "newuser",
#         "password": "password123",
#         "email": "newuser@example.com",
#         "first_name": "New",
#         "last_name": "User",
#     }
#     response = await client.post("/users/create", json=payload)
#     data = response.json()

#     assert response.status_code == 200
#     assert data["username"] == payload["username"]
#     assert data["id"] > 0

# @pytest.mark.asyncio
# async def test_read_user(client: AsyncClient, token_user1: models.Token):
#     headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
#     response = await client.get(f"/users/{token_user1.user_id}", headers=headers)
#     data = response.json()

#     assert response.status_code == 200
#     assert data["id"] == token_user1.user_id

# @pytest.mark.asyncio
# async def test_update_user(client: AsyncClient, token_user1: models.Token):
#     headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
#     update_payload = {
#         "username": "updateduser",
#         "first_name": "Updated",
#         "last_name": "User",
#         "email": "updateduser@example.com"  # Remove the "roles" field
#     }
#     response = await client.put(f"/users/{token_user1.user_id}/update", json=update_payload, headers=headers)
#     data = response.json()

#     assert response.status_code == 200
#     assert data["username"] == update_payload["username"]
#     assert data["first_name"] == update_payload["first_name"]
#     assert data["last_name"] == update_payload["last_name"]
#     assert data["email"] == update_payload["email"]

# @pytest.mark.asyncio
# async def test_delete_user(client: AsyncClient, token_user1: models.Token, session: models.AsyncSession):
#     headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}

#     # Create a new user to be deleted
#     user_info = models.RegisteredUser(
#         username="tobedeleted",
#         password="password123",
#         email="tobedeleted@example.com",
#         first_name="To",
#         last_name="BeDeleted"
#     )

#     new_user = models.DBUser.from_orm(user_info)
#     await new_user.set_password(user_info.password)
#     session.add(new_user)
#     await session.commit()
#     await session.refresh(new_user)

#     # Delete the user
#     response = await client.delete(f"/users/{new_user.id}/delete", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["detail"] == "User deleted successfully"

#     # Clear session to avoid stale objects
#     await session.commit()
#     await session.flush()

#     # Verify the user is deleted
#     deleted_user = await session.get(models.DBUser, new_user.id)
#     assert deleted_user is None  # This should pass now

# @pytest.mark.asyncio
# async def test_delete_user_not_found(client: AsyncClient, token_user1: models.Token):
#     headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
#     response = await client.delete("/users/9999/delete", headers=headers)  # Assuming ID 9999 does not exist
#     assert response.status_code == 404
#     assert response.json()["detail"] == "User not found"

# @pytest.mark.asyncio
# async def test_user_already_exists(client: AsyncClient, token_user1: models.Token):
#     headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
#     payload = {
#         "username": "user1",  # Make sure to use an existing username
#         "password": "password123",
#         "email": "newuser@example.com",
#         "first_name": "New",
#         "last_name": "User",
#     }
#     response = await client.post("/users/create", json=payload, headers=headers)
#     assert response.status_code == 409
#     assert response.json()["detail"] == "This username already exists."

# @pytest.mark.asyncio
# async def test_change_password(client: AsyncClient, token_user1: models.Token):
#     headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
#     change_password_payload = {
#         "current_password": "123456",  # Assuming this is the correct current password
#         "new_password": "newpassword123",
#     }
#     response = await client.put(f"/users/{token_user1.user_id}/change_password", json=change_password_payload, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["detail"] == "Password updated successfully"

#     # Verify that the password was updated by attempting to log in with the new password
#     login_payload = {
#         "username": "user1",  # Use username instead of email
#         "password": "newpassword123",
#     }
#     response = await client.post("/token", data=login_payload)
#     assert response.status_code == 200
#     assert "access_token" in response.json()

# @pytest.mark.asyncio
# async def test_change_password_incorrect_current_password(client: AsyncClient, token_user1: models.Token):
#     headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
#     change_password_payload = {
#         "current_password": "wrongpassword",  # Incorrect current password
#         "new_password": "newpassword123",
#     }
#     response = await client.put(f"/users/{token_user1.user_id}/change_password", json=change_password_payload, headers=headers)
    
#     assert response.status_code == 401
#     assert response.json()["detail"] == "Incorrect password"
