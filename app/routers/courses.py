from fastapi import APIRouter, Depends, HTTPException
from app.schemas.assignments import AssignmentCreate, AssignmentRequest
from app.services.assignments import create_assignment
from app.services.courses import create_course, get_course, get_courses_by_user
from app.schemas.courses import CourseCreate, CoursePydantic
from app.auth.dependencies import RoleChecker, get_current_user, verify_course_creator
from app.models.sysuser import SysUser, RoleEnum

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=CoursePydantic, status_code=201)
async def create_course_endpoint(
    course: CourseCreate,
    current_user: SysUser = Depends(RoleChecker([RoleEnum.PROFESSOR]))
):
    course_data = course.dict()
    course_data["created_by_id"] = current_user.id
    return await create_course(course_data)

@router.get("/{course_id}", response_model=CoursePydantic)
async def get_course_endpoint(course_id: int, course = Depends(verify_course_creator)):
    course = await get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/{course_id}/assignments", status_code=201)
async def create_assignment_endpoint(course_id: int, assignment: AssignmentRequest, current_user: SysUser = Depends(RoleChecker([RoleEnum.PROFESSOR]))):
    assignment = AssignmentCreate(course_id=course_id, **assignment.dict(), created_by_id=current_user.id)
    return await create_assignment(assignment)

@router.get("/")
async def get_courses_by_user_endpoint(current_user: SysUser = Depends(get_current_user)):
    return await get_courses_by_user(current_user.id)