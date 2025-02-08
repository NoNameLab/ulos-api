from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.task_log import TaskLog

TaskLogPydantic = pydantic_model_creator(TaskLog, name="TaskLog")
TaskLogPydanticIn = pydantic_model_creator(TaskLog, name="TaskLogIn", exclude_readonly=True)

class TaskLogRequest(BaseModel):
    log_message: str


class TaskLogCreate(BaseModel):
    task_id: int
    log_message: str