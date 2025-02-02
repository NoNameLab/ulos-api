from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.course import Course
from app.models.sysuser import SysUser, RoleEnum
from app.services.sysusers import get_sysuser

from app.auth import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
token_dep = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(token: token_dep) -> SysUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id = jwt.decode_token(token)
        if not user_id:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    sysuser = await get_sysuser(int(user_id))
    if not sysuser:
        raise credentials_exception

    return sysuser



async def verify_course_creator(course_id: int, current_user: SysUser = Depends(get_current_user)):
    course = await Course.get(id=course_id)
    if course.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return course

class RoleChecker:
    def __init__(self, allowed_roles: list[RoleEnum]):
        self.allowed_roles = allowed_roles

    def __call__(self, sysuser: Annotated[SysUser, Depends(get_current_user)]):
        if sysuser.assigned_role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return sysuser