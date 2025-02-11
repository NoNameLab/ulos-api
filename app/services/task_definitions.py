from app.models.task_definition import TaskDefinition
from app.schemas.task_definitions import TaskDefinitionCreate, TaskDefinitionPydantic

async def create_task_definition(task_definition: TaskDefinitionCreate):
    task_definition_obj = await TaskDefinition.create(**task_definition.model_dump(exclude_unset=True))
    return await TaskDefinitionPydantic.from_tortoise_orm(task_definition_obj)

async def get_task_definitions():
    return await TaskDefinition.all().prefetch_related(
        "stages__processing_stage__container"
    )

async def update_task_definition(task_definition_id: int, task_definition: TaskDefinitionCreate):
    task_definition_obj = await TaskDefinition.get_or_none(id=task_definition_id)
    if not task_definition_obj:
        return None
    await task_definition_obj.update_from_dict(task_definition.model_dump(exclude_unset=True)).save()
    return await TaskDefinitionPydantic.from_tortoise_orm(task_definition_obj)


async def delete_task_definition(task_definition_id: int):
    deleted_count = await TaskDefinition.filter(id=task_definition_id).delete()
    return deleted_count > 0