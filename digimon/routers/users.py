# digimon/routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from .. import models, deps

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
async def get_me(current_user: Annotated[models.User, Depends(deps.get_current_user)]) -> models.User:
    return current_user

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> models.User:
    user = await session.get(models.DBUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return models.User.from_orm(user)

@router.post("/create")
async def create_user(
    user_info: models.UserCreate,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.User:
    existing_user = await session.exec(select(models.DBUser).where(models.DBUser.username == user_info.username))
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    user = models.DBUser.from_orm(user_info)
    await user.set_password(user_info.password)
    session.add(user)
    await session.commit()
    return models.User.from_orm(user)
