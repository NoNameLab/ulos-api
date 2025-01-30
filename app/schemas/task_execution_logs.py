from pydantic import BaseModel, validator
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.task_execution_log import TaskExecutionLog

# Pydantic models for TaskExecutionLog
taskExecutionLog_pydantic = pydantic_model_creator(TaskExecutionLog, name="TaskExecutionLog")
taskExecutionLog_pydanticIn = pydantic_model_creator(TaskExecutionLog, name="TaskExecutionLogIn", exclude_readonly=True)

class TaskExecutionLogCreate(BaseModel):
    task_id: int
    step_name: str = None
    step_status: int = 0
    old_state: int = None
    new_state: int = None
    error_message: str = None
    machine_id: int = None

    @validator("step_status", "old_state", "new_state")
    def validate_statuses(cls, value):
        if value not in {0, 1, 2, 3}:
            raise ValueError("Statuses must be one of 0 (pending), 1 (in progress), 2 (completed), 3 (error)")
        return value
