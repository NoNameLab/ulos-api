from app.models.task_execution_log import TaskExecutionLog
from app.schemas.task_execution_logs import TaskExecutionLogCreate, taskExecutionLog_pydantic


async def create_task_execution_log(log: TaskExecutionLogCreate):
    log_obj = await TaskExecutionLog.create(**log.model_dump(exclude_unset=True))
    return await taskExecutionLog_pydantic.from_tortoise_orm(log_obj)

async def get_task_execution_log(log_id: int):
    return await TaskExecutionLog.get_or_none(id=log_id)

async def update_task_execution_log(log_id: int, log: TaskExecutionLogCreate):
    log_obj = await TaskExecutionLog.get_or_none(id=log_id)
    if not log_obj:
        return None
    await log_obj.update_from_dict(log.model_dump(exclude_unset=True)).save()
    return await taskExecutionLog_pydantic.from_tortoise_orm(log_obj)

async def delete_task_execution_log(log_id: int):
    deleted_count = await TaskExecutionLog.filter(id=log_id).delete()
    return deleted_count > 0