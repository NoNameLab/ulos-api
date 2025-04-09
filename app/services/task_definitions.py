from app.models.task_definition import TaskDefinition
from app.schemas.task_definitions import TaskDefinitionCreate, TaskDefinitionPydantic


async def get_task_definitions():
    return await TaskDefinition.all().prefetch_related(
        "stages__processing_stage__container"
    )


async def get_task_definition(task_definition_id: int):
    task_definition = await TaskDefinition.get_or_none(id=task_definition_id).prefetch_related(
        "stages__processing_stage__container"
    )
    return await TaskDefinitionPydantic.from_tortoise_orm(task_definition) if task_definition else None
