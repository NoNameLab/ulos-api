from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.task import Task

TaskPydantic = pydantic_model_creator(Task, name="Task")
TaskPydanticIn = pydantic_model_creator(Task, name="TaskIn", exclude_readonly=True)

class TaskCreate(BaseModel):
    assignment_id: int
    remote_storage_path: str
    created_by_id: int

