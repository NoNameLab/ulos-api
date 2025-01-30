from fastapi import APIRouter, HTTPException
from app.services.task_execution_logs import create_task_execution_log, get_task_execution_log, update_task_execution_log, delete_task_execution_log
from app.schemas.task_execution_logs import TaskExecutionLogCreate, taskExecutionLog_pydantic

router = APIRouter(prefix="/task-execution-logs", tags=["Task Execution Logs"])

@router.post("/", response_model=taskExecutionLog_pydantic, status_code=201)
async def create_task_execution_log_endpoint(log: TaskExecutionLogCreate):
    """
    Crea un nuevo registro de ejecución de tarea en la base de datos.
    """
    return await create_task_execution_log(log)


@router.get("/{log_id}", response_model=taskExecutionLog_pydantic)
async def get_task_execution_log_endpoint(log_id: int):
    """
    Recupera un registro de ejecución de tarea por su ID.
    """
    log = await get_task_execution_log(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Task execution log not found")
    return log


@router.put("/{log_id}", response_model=taskExecutionLog_pydantic)
async def update_task_execution_log_endpoint(log_id: int, log: TaskExecutionLogCreate):
    """
    Actualiza un registro de ejecución de tarea existente.
    """
    updated_log = await update_task_execution_log(log_id, log)
    if not updated_log:
        raise HTTPException(status_code=404, detail="Task execution log not found")
    return updated_log


@router.delete("/{log_id}", status_code=204)
async def delete_task_execution_log_endpoint(log_id: int):
    """
    Elimina un registro de ejecución de tarea por su ID.
    """
    if not await delete_task_execution_log(log_id):
        raise HTTPException(status_code=404, detail="Task execution log not found")
    return {"detail": "Task execution log deleted successfully"}
