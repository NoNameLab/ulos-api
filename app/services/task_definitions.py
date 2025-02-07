from app.models.task_definition import TaskDefinition
from app.schemas.task_definitions import TaskDefinitionCreate, TaskDefinitionPydantic

async def create_task_definition(task_definition: TaskDefinitionCreate):
    task_definition_obj = await TaskDefinition.create(**task_definition.model_dump(exclude_unset=True))
    return await TaskDefinitionPydantic.from_tortoise_orm(task_definition_obj)

async def get_task_definitions():
    return await TaskDefinition.all().prefetch_related(
        "stages__processing_stage__container"
    )
