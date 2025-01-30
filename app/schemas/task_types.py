from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.task_type import TaskType

# Pydantic Schemas
taskType_pydantic = pydantic_model_creator(TaskType, name="TaskType")
taskType_pydanticIn = pydantic_model_creator(TaskType, name="TaskTypeIn", exclude_readonly=True)

class TaskTypeCreate(BaseModel):
    name: str

    @staticmethod
    def validate_name(value: str):
        if len(value.strip()) == 0:
            raise ValueError("Task type name cannot be empty")
        return value
