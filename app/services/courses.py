from fastapi import HTTPException
from app.models.course import Course
from app.models.course_user import CourseUser, RoleEnum
from app.models.sysuser import SysUser
from app.schemas.courses import CoursePydantic

import secrets
import pandas as pd
from app.auth.hashing import get_password_hash
from app.helpers.email_utils import send_registration_email

async def create_course(course: dict):
    course_obj = await Course.create(**course)
    return await CoursePydantic.from_tortoise_orm(course_obj)


async def get_course(course_id: int):
    course = await Course.get_or_none(id=course_id)
    return await CoursePydantic.from_tortoise_orm(course) if course else None


async def get_courses_by_user(user_id):
    return await Course.filter(users__user_id=user_id).all()



async def process_excel_file(df: pd.DataFrame, course, background_tasks):
    required_columns = ["ID de alumno", "Apellidos", "Nombres", "Email"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Columna requerida '{col}' no encontrada en el archivo Excel.")

    for _, row in df.iterrows():
        email = row.get("Email")
        if not email:
            continue

        generated_password = secrets.token_urlsafe(8)
        hashed_password = get_password_hash(generated_password)

        user, created = await SysUser.get_or_create(
            email=email,
            defaults={
                "password": hashed_password
            }
        )

        if created:
            background_tasks.add_task(send_registration_email, user.email, generated_password, course.course_name)


        await CourseUser.get_or_create(
            course=course,
            user=user,
            defaults={"course_role": RoleEnum.STUDENT}
        )




async def remove_user_from_course(course_id: int, user_id: int) -> None:
    course = await Course.get_or_none(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    user = await SysUser.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    association = await CourseUser.get_or_none(course=course, user=user)
    if not association:
        raise HTTPException(status_code=404, detail="El usuario no está inscrito en este curso")

    await association.delete()


async def get_students_by_course(course_id: int):
    course = await Course.get_or_none(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    course_users = await CourseUser.filter(course=course, course_role=RoleEnum.STUDENT).prefetch_related("user").all()
    students = [cu.user for cu in course_users]
    return students
