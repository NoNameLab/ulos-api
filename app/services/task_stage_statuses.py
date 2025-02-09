from app.models.task_stage_status import TaskStageStatus
from app.schemas.task_stage_statuses import TaskStageStatusCreate, TaskStageStatusPydantic


async def create_task_stage_status(task_stage_status: TaskStageStatusCreate):
    task_stage_status_obj = await TaskStageStatus.create(**task_stage_status.model_dump())
    return await TaskStageStatusPydantic.from_tortoise_orm(task_stage_status_obj)