from fastapi import APIRouter, HTTPException, Depends
from app.auth.dependencies import get_current_user
from app.models.sysuser import SysUser
from app.schemas.auth import Token, CourseSelection, CoursesResponse
from app.schemas.sysusers import SysUserLogin
from app.services.sysusers import login_user, get_user_courses, select_course_for_user
from app.auth.jwt import create_access_token

router = APIRouter()

@router.post("/login")
async def login_user_endpoint(user: SysUserLogin):
    login_data = await login_user(user)
    if not login_data:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_courses = await get_user_courses(login_data["user_id"])

    token = create_access_token(data={"sub": str(login_data["user_id"])})

    return {
        "access_token": token,
        "token_type": "bearer",
        "courses": user_courses
    }

@router.post("/select_course", response_model=Token)
async def select_course(course_selection: CourseSelection, current_user: SysUser = Depends(get_current_user)):
    course_info = await select_course_for_user(current_user.id, course_selection.course_id)
    if not course_info:
        raise HTTPException(status_code=403, detail="User is not enrolled in the selected course")

    token_data = {
        "sub": str(current_user.id),
        "active_course_id": course_selection.course_id,
        "active_course_role": course_info["course_role"]
    }
    new_token = create_access_token(data=token_data)
    return {"access_token": new_token, "token_type": "bearer"}
