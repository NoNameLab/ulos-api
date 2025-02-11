from app.models.course import Course
from app.schemas.courses import CoursePydantic


async def create_course(course: dict):
    course_obj = await Course.create(**course)
    return await CoursePydantic.from_tortoise_orm(course_obj)


async def get_course(course_id: int):
    course = await Course.get_or_none(id=course_id)
    return await CoursePydantic.from_tortoise_orm(course) if course else None


async def get_courses_by_user(user_id):
    return await Course.filter(users__user_id=user_id).all()