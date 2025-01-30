from app.models.task_type import TaskType
from app.schemas.task_types import TaskTypeCreate, taskType_pydantic

async def create_task_type(task_type: TaskTypeCreate):
    """Crea un nuevo tipo de tarea."""
    task_type_obj = await TaskType.create(**task_type.model_dump(exclude_unset=True))
    return await taskType_pydantic.from_tortoise_orm(task_type_obj)

async def get_task_type(task_type_id: int):
    """Recupera un tipo de tarea por su ID."""
    task_type = await TaskType.get_or_none(id=task_type_id)
    return await taskType_pydantic.from_tortoise_orm(task_type) if task_type else None

async def update_task_type(task_type_id: int, task_type: TaskTypeCreate):
    """Actualiza un tipo de tarea existente."""
    task_type_obj = await TaskType.get_or_none(id=task_type_id)
    if not task_type_obj:
        return None
    await task_type_obj.update_from_dict(task_type.model_dump(exclude_unset=True)).save()
    return await taskType_pydantic.from_tortoise_orm(task_type_obj)

async def delete_task_type(task_type_id: int) -> bool:
    """Elimina un tipo de tarea por su ID."""
    deleted_count = await TaskType.filter(id=task_type_id).delete()
    return deleted_count > 0
