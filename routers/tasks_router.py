# C:\Uuu\FastAPIULOS\routers\tasks_router.py

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, validator
from tortoise.contrib.pydantic import pydantic_model_creator
from models import Task, TaskExecutionLog
from typing import List, Dict
import random

router = APIRouter()

# Esquemas Pydantic para Task
Task_Pydantic = pydantic_model_creator(Task, name="Task")
TaskIn_Pydantic = pydantic_model_creator(Task, name="TaskIn", exclude_readonly=True)

# Esquema Pydantic para TaskExecutionLog
TaskExecutionLog_Pydantic = pydantic_model_creator(TaskExecutionLog, name="TaskExecutionLog")

# Esquema basico para respuestas mas simples 
class TaskBasic(BaseModel):
    task_id: int
    file_name: str = None
    state: int

# --------------------------------------------------
# Nuevo: Agrupacion por estado y filtrado por estado
# --------------------------------------------------

@router.get("/group_by_state", response_model=Dict[str, List[int]])
async def group_tasks_by_state():
    """
    Agrupa las tareas por su estado ('state') y devuelve solo los IDs de las tareas.
    """
    tasks = await Task.all()
    grouped_tasks = {
        "pending": [task.task_id for task in tasks if task.state == 0],
        "in_progress": [task.task_id for task in tasks if task.state == 1],
        "completed": [task.task_id for task in tasks if task.state == 2],
        "failed": [task.task_id for task in tasks if task.state == 3],
    }
    return grouped_tasks


@router.get("/filter_by_state", response_model=List[TaskBasic])
async def filter_tasks_by_state(
    state: int = Query(..., description="State of the task (0: pending, 1: in progress, 2: completed, 3: failed)")
):
    """
    Filtra las tareas por su estado ('state') y devuelve información básica.
    """
    if state not in {0, 1, 2, 3}:
        raise HTTPException(status_code=400, detail="State must be one of 0 (pending), 1 (in progress), 2 (completed), 3 (failed)")

    tasks = await Task.filter(state=state).values("task_id", "file_name", "state")
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found with the specified state")
    return tasks

# Mapping de los estados
STATE_NAMES = {
    0: "Pending",
    1: "In Progress",
    2: "Completed",
    3: "Failed"
}

# -----------------------------------------
# Nuevo: Estados con nombres
# -----------------------------------------

@router.get("/task_states", response_model=Dict[int, str])
async def get_task_states():
    """
    Returns a mapping of task state numbers to their corresponding names.
    """
    return STATE_NAMES

# ------------------------------------
# Nuevo: Estados de tareas con nombres
# ------------------------------------

class TaskWithStateName(BaseModel):
    task_id: int
    file_name: str = None
    state: str

@router.get("/tasks_with_state_names", response_model=List[TaskWithStateName])
async def get_tasks_with_state_names():
    """
    Fetches tasks and replaces state numbers with human-readable state names.
    """
    tasks = await Task.all().values("task_id", "file_name", "state")

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")

    # Cambia el estado con el nombre que representa
    tasks_with_names = [
        {
            "task_id": task["task_id"],
            "file_name": task["file_name"],
            "state": STATE_NAMES.get(task["state"], "Unknown")
        }
        for task in tasks
    ]

    return tasks_with_names

class TaskCreate(BaseModel):
    user_id: int
    file_name: str = None
    ftp_file_path: str = None
    task_type_id: int
    parsed_status: int = 0
    executed_status: int = 0
    state: int = 0
    requeue_count: int = 0
    feedback: str = None

    @validator("parsed_status", "executed_status", "state")
    def validate_status(cls, value):
        if value not in {0, 1, 2, 3}:
            raise ValueError("Status must be one of 0 (pending), 1 (in progress), 2 (completed), 3 (failed)")
        return value

# CRUD Endpoints
@router.post("/", response_model=Task_Pydantic, status_code=201)
async def create_task(task: TaskCreate):
    """
    Crea una nueva tarea en la base de datos.
    """
    task_obj = await Task.create(**task.dict(exclude_unset=True))
    return await Task_Pydantic.from_tortoise_orm(task_obj)


@router.get("/{task_id}", response_model=Task_Pydantic)
async def get_task(task_id: int):
    """
    Recupera una tarea por su ID.
    """
    task = await Task.get_or_none(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await Task_Pydantic.from_tortoise_orm(task)


@router.put("/{task_id}", response_model=Task_Pydantic)
async def update_task(task_id: int, task: TaskCreate):
    """
    Actualiza una tarea existente.
    """
    task_obj = await Task.get_or_none(task_id=task_id)
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    await task_obj.update_from_dict(task.dict(exclude_unset=True)).save()
    return await Task_Pydantic.from_tortoise_orm(task_obj)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """
    Elimina una tarea por su ID.
    """
    deleted_count = await Task.filter(task_id=task_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}


# Cambiar status 
class StatusUpdate(BaseModel):
    status: int

    @validator("status")
    def validate_status(cls, value):
        if value not in {0, 1, 2, 3}:
            raise ValueError("Status must be one of 0 (pending), 1 (in progress), 2 (completed), 3 (failed)")
        return value

# Funcion helper para crear un registro en el log
async def create_log_entry(task_id: int, old_state: int, new_state: int, error_message: str = None):
    await TaskExecutionLog.create(
        task_id=task_id,
        step_name="Status Update",
        step_status=new_state,
        old_state=old_state,
        new_state=new_state,
        error_message=error_message
    )

@router.patch("/{task_id}/parsed_status", response_model=Task_Pydantic)
async def update_parsed_status(task_id: int, status_update: StatusUpdate):
    """
    Actualiza el 'parsed_status' de una tarea por su ID y registra el cambio.
    """
    task = await Task.get_or_none(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    old_status = task.parsed_status
    task.parsed_status = status_update.status
    await task.save()
    
    await create_log_entry(task_id, old_state=old_status, new_state=task.parsed_status)
    return await Task_Pydantic.from_tortoise_orm(task)


@router.patch("/{task_id}/executed_status", response_model=Task_Pydantic)
async def update_executed_status(task_id: int, status_update: StatusUpdate):
    """
    Actualiza el 'executed_status' de una tarea por su ID y registra el cambio.
    """
    task = await Task.get_or_none(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    old_status = task.executed_status
    task.executed_status = status_update.status
    await task.save()
    
    await create_log_entry(task_id, old_state=old_status, new_state=task.executed_status)
    return await Task_Pydantic.from_tortoise_orm(task)


@router.patch("/{task_id}/state", response_model=Task_Pydantic)
async def update_state(task_id: int, status_update: StatusUpdate):
    """
    Actualiza el 'state' de una tarea por su ID y registra el cambio.
    """
    task = await Task.get_or_none(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    old_status = task.state
    task.state = status_update.status
    await task.save()
    
    await create_log_entry(task_id, old_state=old_status, new_state=task.state)
    return await Task_Pydantic.from_tortoise_orm(task)

# ----------------------------
# Nuevo: Simulacion de errores
# -----------------------------

@router.post("/{task_id}/simulate_parsed_error")
async def simulate_parsed_error(task_id: int):
    """
    Simula un error específico al actualizar 'parsed_status' y registra el error.
    """
    task = await Task.get_or_none(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = task.parsed_status
    error_message = "Unexpected error occurred while updating parsed status."

    # Simular siempre un error específico
    await TaskExecutionLog.create(
        task_id=task_id,
        step_name="parsed error",
        step_status=3,  # 'Fallido' status
        old_state=old_status,
        new_state=3,
        error_message=error_message
    )
    
    raise HTTPException(status_code=500, detail=error_message)

@router.post("/{task_id}/simulate_executed_error")
async def simulate_executed_error(task_id: int):
    """
    Simula un error específico al actualizar 'executed_status' y registra el error.
    """
    task = await Task.get_or_none(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = task.executed_status
    error_message = "Unexpected error occurred while updating executed status."

    # Crear un registro de error en los logs
    await TaskExecutionLog.create(
        task_id=task_id,
        step_name="executed error",
        step_status=3,  # 'Fallido' status
        old_state=old_status,
        new_state=3,
        error_message=error_message
    )

    raise HTTPException(status_code=500, detail=error_message)


@router.post("/{task_id}/simulate_state_error")
async def simulate_state_error(task_id: int):
    """
    Simula un error específico al actualizar 'state' y registra el error.
    """
    task = await Task.get_or_none(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = task.state
    error_message = "Unexpected error occurred while updating task state."

    # Crear un registro de error en los logs
    await TaskExecutionLog.create(
        task_id=task_id,
        step_name="state error",
        step_status=3,  # 'Fallido' status
        old_state=old_status,
        new_state=3,
        error_message=error_message
    )

    raise HTTPException(status_code=500, detail=error_message)


