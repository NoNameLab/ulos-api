from app.models.stage_by_task_definition import StageByTaskDefinition
from app.schemas.stages_by_task_definitions import StageByTaskDefinitionCreate, StageByTaskDefinitionPydantic

async def create_stage_by_task_definition(stage_by_task_definition: StageByTaskDefinitionCreate):
    stage_by_task_definition_obj = await StageByTaskDefinition.create(**stage_by_task_definition.model_dump(exclude_unset=True))
    return await StageByTaskDefinitionPydantic.from_tortoise_orm(stage_by_task_definition_obj)

async def get_stages_by_task_definition(task_definition_id: int):
    stages = await StageByTaskDefinition.filter(
        task_definition_id=task_definition_id
    ).prefetch_related("processing_stage__container")

    return [stage.processing_stage for stage in stages]