# digimon/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import jwt

from . import models, security, config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
settings = config.get_settings()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[models.AsyncSession, Depends(models.get_session)]) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = await session.get(models.DBUser, user_id)
    if user is None:
        raise credentials_exception

    return user

class RoleChecker:
    def __init__(self, *allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[models.User, Depends(get_current_user)]):
        if not any(role in self.allowed_roles for role in user.roles):
            raise HTTPException(status_code=403, detail="Role not permitted")
