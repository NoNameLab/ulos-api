from app.models.task_log import TaskLog
from app.schemas.task_logs import TaskLogCreate, TaskLogPydantic

async def create_task_log(task_log: TaskLogCreate):
    task_log_obj = await TaskLog.create(**task_log.model_dump(exclude_unset=True))
    return await TaskLogPydantic.from_tortoise_orm(task_log_obj)