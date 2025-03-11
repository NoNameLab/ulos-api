from fastapi import APIRouter, HTTPException
from app.models.sysuser import SysUser
from app.schemas.auth import Token
from app.schemas.sysusers import SysUserCreate, SysUserLogin
from app.services.sysusers import create_sysuser, login_user

router = APIRouter()

@router.post("/register", response_model=dict)
async def register_user(user: SysUserCreate):
    existing_user = await SysUser.get_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_sysuser(user)
    return {"message": "User registered successfully", "user": new_user}

@router.post("/login")
async def login_user_endpoint(user: SysUserLogin):
    login_data = await login_user(user)

    if not login_data:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return login_data
