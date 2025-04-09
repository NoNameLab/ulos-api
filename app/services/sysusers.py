from app.models.sysuser import SysUser
from app.models.course_user import CourseUser
from app.schemas.sysusers import SysUserCreate, SysUserLogin, SysUserPydantic
from app.auth.hashing import get_password_hash, verify_password
from app.auth.jwt import create_access_token

async def create_sysuser(user: SysUserCreate):
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    sysuser_obj = await SysUser.create(**user_data)
    return await SysUserPydantic.from_tortoise_orm(sysuser_obj)

async def authenticate_user(user: SysUserLogin):
    sysuser = await SysUser.get_or_none(email=user.email)
    if not sysuser or not verify_password(user.password, sysuser.password):
        return None
    return sysuser

async def login_user(user: SysUserLogin):
    sysuser = await authenticate_user(user)
    if not sysuser:
        return None
    token = create_access_token(data={"sub": str(sysuser.id)})
    return {"access_token": token, "user_id": sysuser.id}

async def get_sysuser(sysuser_id: int):
    sysuser = await SysUser.get_or_none(id=sysuser_id)
    return await SysUserPydantic.from_tortoise_orm(sysuser)

async def get_user_courses(user_id: int):
    courses = await CourseUser.filter(user_id=user_id).prefetch_related("course").all()
    course_list = []
    for cu in courses:
        course_list.append({
            "course_id": cu.course.id,
            "course_name": cu.course.course_name,
            "course_role": cu.course_role
        })
    return course_list

async def select_course_for_user(user_id: int, course_id: int):
    course_user = await CourseUser.get_or_none(user_id=user_id, course_id=course_id)
    if course_user:
        return {"course_role": course_user.course_role}
    return None
