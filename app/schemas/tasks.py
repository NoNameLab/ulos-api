from pydantic import BaseModel, validator
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.task import Task

task_pydantic = pydantic_model_creator(Task, name="Task")
task_pydanticIn = pydantic_model_creator(Task, name="TaskIn", exclude_readonly=True)

class TaskBasic(BaseModel):
    task_id: int
    file_name: str = None
    state: int

class TaskWithStateName(BaseModel):
    task_id: int
    file_name: str = None
    state: str

class StatusUpdate(BaseModel):
    status: int

    @validator("status")
    def validate_status(cls, value):
        if value not in {0, 1, 2, 3}:
            raise ValueError("Status must be one of 0 (pending), 1 (in progress), 2 (completed), 3 (failed)")
        return value

class TaskCreate(BaseModel):
    user_id: int
    file_name: str = None
    ftp_file_path: str = None
    task_type_id: int
    parsed_status: int = 0
    executed_status: int = 0
    state: int = 0
    requeue_count: int = 0
    feedback: str = None

    @validator("parsed_status", "executed_status", "state")
    def validate_status(cls, value):
        if value not in {0, 1, 2, 3}:
            raise ValueError("Status must be one of 0 (pending), 1 (in progress), 2 (completed), 3 (failed)")
        return value
