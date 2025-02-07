from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.stage_by_task_definition import StageByTaskDefinition

StageByTaskDefinitionPydantic = pydantic_model_creator(StageByTaskDefinition, name="StageByTaskDefinition")
StageByTaskDefinitionPydanticIn = pydantic_model_creator(StageByTaskDefinition, name="StageByTaskDefinitionIn", exclude_readonly=True)

class StageByTaskDefinitionCreate(BaseModel):
    task_definition_id: int
    processing_stage_id: int
