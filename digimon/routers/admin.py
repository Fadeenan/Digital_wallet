# digimon/routers/admin.py

from fastapi import APIRouter, Depends
from ..deps import RoleChecker

router = APIRouter()

@router.get("/admin", dependencies=[Depends(RoleChecker("admin"))])
async def admin_route():
    return {"message": "Admin access granted"}
