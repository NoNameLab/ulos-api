import io
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
import pandas as pd
from app.models.course import Course
from app.models.course_user import RoleEnum
from app.schemas.assignments import AssignmentCreate, AssignmentRequest
from app.services.assignments import create_assignment, get_assignments_by_course
from app.services.courses import create_course, get_course, get_courses_by_user, get_students_by_course, process_excel_file, remove_user_from_course
from app.schemas.courses import CourseCreate, CoursePydantic
from app.auth.dependencies import RoleChecker, get_current_user, verify_course_professor
from app.models.sysuser import SysUser

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
async def get_course_endpoint(course_id: int, course = Depends(verify_course_professor)):
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


@router.get("/{course_id}/assignments")
async def get_assignments_by_course_endpoint(course_id: int):
    return await get_assignments_by_course(course_id)


@router.post("/{course_id}/upload_students")
async def upload_students(course_id: int, background_tasks: BackgroundTasks,  file: UploadFile = File(...)):
    course = await Course.get_or_none(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    try:
        contents = await file.read()
        excel_data = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Error al leer el archivo Excel")

    try:
        await process_excel_file(excel_data, course, background_tasks)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="Error al procesar el archivo")

    return {"message": "Estudiantes añadidos correctamente"}


@router.delete("/{course_id}/users/{user_id}")
async def delete_user_from_course(course_id: int, user_id: int):
    await remove_user_from_course(course_id, user_id)
    return {"message": "Usuario eliminado del curso correctamente"}



@router.get("/{course_id}/students")
async def get_students_by_course_endpoint(course_id: int):
    return await get_students_by_course(course_id)