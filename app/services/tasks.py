from app.models.task import Task
from app.schemas.tasks import TaskCreate, TaskPydantic
from app.services.processing_stages import get_processing_stage_by_name
from app.services.processing_statuses import get_processing_status
from app.services.task_stage_statuses import get_task_stage_status


async def create_task(task: TaskCreate):
    task_obj = await Task.create(**task.model_dump(exclude_unset=True))
    return await TaskPydantic.from_tortoise_orm(task_obj)


async def get_tasks():
    return await TaskPydantic.from_queryset(Task.all())


async def get_task(task_id: int):
    task = await Task.get_or_none(id=task_id)
    return await TaskPydantic.from_tortoise_orm(task) if task else None


async def get_task_by_assignment_and_user(assignment_id: int, user_id: int):
    task = await Task.get_or_none(assignment_id=assignment_id, created_by_id=user_id)
    return await TaskPydantic.from_tortoise_orm(task) if task else None


async def update_task(task_id: int, stage_status_updates: dict):
    for stage_name, new_status_id in stage_status_updates.items():
        stage = await get_processing_stage_by_name(stage_name)
        if not stage:
            raise ValueError(f"Stage '{stage_name}' not found")

        task_stage_status = await get_task_stage_status(task_id, stage.id)
        if not task_stage_status:
            raise ValueError(
                f"TaskStageStatus not found for stage '{stage_name}' in task {task_id}")

        new_status = await get_processing_status(new_status_id)
        if not new_status:
            raise ValueError(
                f"ProcessingStatus with id {new_status_id} not found")

        task_stage_status.processing_status = new_status
        await task_stage_status.save()

    return await TaskPydantic.from_queryset_single(Task.get(id=task_id))
