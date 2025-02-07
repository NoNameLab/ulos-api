from app.models.stage_by_task_definition import StageByTaskDefinition
from app.schemas.stages_by_task_definitions import StageByTaskDefinitionCreate, StageByTaskDefinitionPydantic

async def create_stage_by_task_definition(stage_by_task_definition: StageByTaskDefinitionCreate):
    stage_by_task_definition_obj = await StageByTaskDefinition.create(**stage_by_task_definition.dict())
    return await StageByTaskDefinitionPydantic.from_tortoise_orm(stage_by_task_definition_obj)