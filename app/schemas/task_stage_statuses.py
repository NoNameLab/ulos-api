from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.task_stage_status import TaskStageStatus

TaskStageStatusPydantic = pydantic_model_creator(TaskStageStatus, name="TaskStageStatus")
TaskStageStatusPydanticIn = pydantic_model_creator(TaskStageStatus, name="TaskStageStatusIn", exclude_readonly=True)

class TaskStageStatusCreate(BaseModel):
    task_id: int
    processing_stage_id: int
    processing_status_id: int = Field(default=1)