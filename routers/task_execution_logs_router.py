# C:\Uuu\FastAPIULOS\routers\task_execution_logs_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from tortoise.contrib.pydantic import pydantic_model_creator
from models import TaskExecutionLog

router = APIRouter()

# Esquemas Pydantic para TaskExecutionLog
TaskExecutionLog_Pydantic = pydantic_model_creator(TaskExecutionLog, name="TaskExecutionLog")
TaskExecutionLogIn_Pydantic = pydantic_model_creator(TaskExecutionLog, name="TaskExecutionLogIn", exclude_readonly=True)

class TaskExecutionLogCreate(BaseModel):
    task_id: int
    step_name: str = None
    step_status: int = 0
    old_state: int = None
    new_state: int = None
    error_message: str = None
    machine_id: int = None

    @validator("step_status", "old_state", "new_state")
    def validate_statuses(cls, value):
        if value not in {0, 1, 2, 3}:
            raise ValueError("Statuses must be one of 0 (pending), 1 (in progress), 2 (completed), 3 (error)")
        return value


@router.post("/", response_model=TaskExecutionLog_Pydantic, status_code=201)
async def create_task_execution_log(log: TaskExecutionLogCreate):
    """
    Crea un nuevo registro de ejecución de tarea en la base de datos.
    """
    log_obj = await TaskExecutionLog.create(**log.dict(exclude_unset=True))
    return await TaskExecutionLog_Pydantic.from_tortoise_orm(log_obj)


@router.get("/{log_id}", response_model=TaskExecutionLog_Pydantic)
async def get_task_execution_log(log_id: int):
    """
    Recupera un registro de ejecución de tarea por su ID.
    """
    log = await TaskExecutionLog.get_or_none(log_id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Task execution log not found")
    return await TaskExecutionLog_Pydantic.from_tortoise_orm(log)


@router.put("/{log_id}", response_model=TaskExecutionLog_Pydantic)
async def update_task_execution_log(log_id: int, log: TaskExecutionLogCreate):
    """
    Actualiza un registro de ejecución de tarea existente.
    """
    log_obj = await TaskExecutionLog.get_or_none(log_id=log_id)
    if not log_obj:
        raise HTTPException(status_code=404, detail="Task execution log not found")
    await log_obj.update_from_dict(log.dict(exclude_unset=True)).save()
    return await TaskExecutionLog_Pydantic.from_tortoise_orm(log_obj)


@router.delete("/{log_id}", status_code=204)
async def delete_task_execution_log(log_id: int):
    """
    Elimina un registro de ejecución de tarea por su ID.
    """
    deleted_count = await TaskExecutionLog.filter(log_id=log_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Task execution log not found")
    return {"detail": "Task execution log deleted successfully"}
