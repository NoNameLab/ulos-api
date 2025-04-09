from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.course_user import CourseUser, RoleEnum
from app.models.sysuser import SysUser
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
        payload = jwt.decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception

        active_course_id = payload.get("active_course_id")
        active_course_role = payload.get("active_course_role")
    except Exception:
        raise credentials_exception

    sysuser = await get_sysuser(int(user_id))
    if not sysuser:
        raise credentials_exception

    object.__setattr__(sysuser, "active_course_id", active_course_id)
    object.__setattr__(sysuser, "active_course_role", active_course_role)

    return sysuser

async def verify_course_professor(
    course_id: int, current_user: SysUser = Depends(get_current_user)
):
    course_enrollment = await CourseUser.get_or_none(course_id=course_id, user_id=current_user.id)

    if not course_enrollment or course_enrollment.course_role != RoleEnum.PROFESSOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a professor in this course"
        )
    return course_enrollment


class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: SysUser = Depends(get_current_user)):
        if not hasattr(current_user, "active_course_role") or current_user.active_course_role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user
