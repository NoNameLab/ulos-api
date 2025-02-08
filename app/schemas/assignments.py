from pydantic import BaseModel
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.assignment import Assignment

AssignmentPydantic = pydantic_model_creator(Assignment, name="Assignment")
AssignmentPydanticIn = pydantic_model_creator(Assignment, name="AssignmentIn", exclude_readonly=True)

class AssignmentCreate(BaseModel):
    course_id: int
    task_definition_id: int
    assignment_name: str
    assignment_description: str
    assignment_start_date: datetime
    assignment_end_date: datetime
    created_by_id: int