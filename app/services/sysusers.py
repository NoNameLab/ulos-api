from app.models.sysuser import SysUser
from app.schemas.sysusers import SysUserCreate, SysUserLogin, SysUserPydantic
from app.auth.hashing import get_password_hash, verify_password
from app.auth.jwt import create_access_token
from app.schemas.auth import Token

async def create_sysuser(user: SysUserCreate):
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    sysuser_obj = await SysUser.create(**user_data)
    return await SysUserPydantic.from_tortoise_orm(sysuser_obj)

async def authenticate_user(user: SysUserLogin):
    """Authenticate a user"""
    sysuser = await SysUser.get_or_none(email=user.email)
    if not sysuser or not verify_password(user.password, sysuser.password):
        return None
    return sysuser

async def login_user(user: SysUserLogin):
    """Login a user and return a token along with the assigned role"""
    sysuser = await authenticate_user(user)
    if not sysuser:
        return None

    access_token = create_access_token(data={"sub": str(sysuser.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": sysuser.assigned_role
    }

async def get_sysuser(sysuser_id):
    """Get a user by id"""
    sysuser = await SysUser.get_or_none(id=sysuser_id)
    return await SysUserPydantic.from_tortoise_orm(sysuser)
