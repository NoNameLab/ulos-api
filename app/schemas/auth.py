from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class CourseSelection(BaseModel):
    course_id: int

class CoursesResponse(BaseModel):
    courses: list[dict]