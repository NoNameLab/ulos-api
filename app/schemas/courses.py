from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.course import Course

CoursePydantic = pydantic_model_creator(Course, name="Course")
CoursePydanticIn = pydantic_model_creator(Course, name="CourseIn", exclude_readonly=True)

class CourseCreate(BaseModel):
    course_name: str