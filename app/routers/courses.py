from fastapi import APIRouter, Depends, HTTPException
from app.services.courses import create_course, get_course
from app.schemas.courses import CourseCreate, course_pydantic
from app.auth.dependencies import RoleChecker, verify_course_creator
from app.models.sysuser import SysUser, RoleEnum

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=course_pydantic, status_code=201)
async def create_course_endpoint(
    course: CourseCreate,
    current_user: SysUser = Depends(RoleChecker([RoleEnum.PROFESSOR]))
):
    course_data = course.dict()
    course_data["created_by_id"] = current_user.id
    return await create_course(course_data)

@router.get("/{course_id}", response_model=course_pydantic)
async def get_course_endpoint(course_id: int, course = Depends(verify_course_creator)):
    course = await get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course