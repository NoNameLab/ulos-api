from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.task_definition import TaskDefinition
from app.schemas.processing_stages import ProcessingStageRequest

TaskDefinitionPydantic = pydantic_model_creator(TaskDefinition, name="TaskDefinition")
TaskDefinitionPydanticIn = pydantic_model_creator(TaskDefinition, name="TaskDefinitionIn", exclude_readonly=True)

class TaskDefinitionRequest(BaseModel):
    type_name: str
    type_description: str
    stages: list[ProcessingStageRequest]

class TaskDefinitionCreate(BaseModel):
    type_name: str
    type_description: str
    created_by_id: int