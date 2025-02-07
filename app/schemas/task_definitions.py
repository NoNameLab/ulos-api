from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.task_definition import TaskDefinition
from app.schemas.processing_stages import ProcessingStageRequest

TaskDefinitionPydantic = pydantic_model_creator(TaskDefinition, name="TaskDefinition")
TaskDefinitionPydanticIn = pydantic_model_creator(TaskDefinition, name="TaskDefinitionIn", exclude_readonly=True)

class TaskDefinitionRequest(BaseModel):
    definition_name: str
    definition_description: str
    stages: list[ProcessingStageRequest]

class TaskDefinitionCreate(BaseModel):
    definition_name: str
    definition_description: str
    created_by_id: int