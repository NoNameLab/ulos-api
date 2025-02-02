from app.models.course import Course
from app.schemas.courses import course_pydantic


async def create_course(course: dict):
    course_obj = await Course.create(**course)
    return await course_pydantic.from_tortoise_orm(course_obj)


async def get_course(course_id: int):
    course = await Course.get_or_none(id=course_id)
    return await course_pydantic.from_tortoise_orm(course) if course else None