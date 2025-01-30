from typing import Dict, List
from fastapi import APIRouter, HTTPException, Query
from app.services.tasks import create_task, filter_tasks_by_state, get_task, get_task_states, get_tasks_with_state_names, group_tasks_by_state, simulate_executed_error, simulate_parsed_error, simulate_state_error, update_task, delete_task, update_parsed_status, update_executed_status, update_state
from app.schemas.tasks import TaskBasic, TaskCreate, StatusUpdate, task_pydantic, TaskWithStateName

router = APIRouter()

@router.post("/", response_model=task_pydantic, status_code=201)
async def create_new_task_endpoint(task: TaskCreate):
    return await create_task(task)

@router.get("/{task_id}", response_model=task_pydantic)
async def get_single_task_endpoint(task_id: int):
    return await get_task(task_id)

@router.put("/{task_id}", response_model=task_pydantic)
async def update_single_task_endpoint(task_id: int, task: TaskCreate):
    return await update_task(task_id, task)

@router.delete("/{task_id}", status_code=204)
async def delete_single_task_endpoint(task_id: int):
    return await delete_task(task_id)

@router.patch("/{task_id}/parsed_status", response_model=task_pydantic)
async def update_task_parsed_status_endpoint(task_id: int, status_update: StatusUpdate):
    return await update_parsed_status(task_id, status_update)

@router.patch("/{task_id}/executed_status", response_model=task_pydantic)
async def update_task_executed_status_endpoint(task_id: int, status_update: StatusUpdate):
    return await update_executed_status(task_id, status_update)

@router.patch("/{task_id}/state", response_model=task_pydantic)
async def update_task_state_endpoint(task_id: int, status_update: StatusUpdate):
    return await update_state(task_id, status_update)

@router.get("/group_by_state", response_model=Dict[str, List[int]])
async def group_tasks_by_state_endpoint():
    """
    Agrupa las tareas por su estado ('state') y devuelve solo los IDs de las tareas.
    """
    return await group_tasks_by_state()

@router.get("/filter_by_state", response_model=List[TaskBasic])
async def filter_tasks_by_state_endpoint(
    state: int = Query(..., description="State of the task (0: pending, 1: in progress, 2: completed, 3: failed)")
):
    """
    Filtra las tareas por su estado ('state') y devuelve información básica.
    """
    tasks = await filter_tasks_by_state(state)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found with the specified state")
    return tasks

@router.get("/task_states", response_model=Dict[int, str])
async def get_task_states_endpoint():
    """
    Returns a mapping of task state numbers to their corresponding names.
    """
    return await get_task_states()

@router.get("/tasks_with_state_names", response_model=List[TaskWithStateName])
async def get_tasks_with_state_names_endpoint():
    """
    Fetches tasks and replaces state numbers with human-readable state names.
    """
    tasks_with_names = await get_tasks_with_state_names()
    if not tasks_with_names:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks_with_names

@router.post("/{task_id}/simulate_parsed_error")
async def simulate_parsed_error_endpoint(task_id: int):
    """
    Simula un error específico al actualizar 'parsed_status' y registra el error.
    """
    error_message = await simulate_parsed_error(task_id)
    if not error_message:
        raise HTTPException(status_code=404, detail="Task not found")
    
    raise HTTPException(status_code=500, detail=error_message)

@router.post("/{task_id}/simulate_executed_error")
async def simulate_executed_error_endpoint(task_id: int):
    """
    Simula un error específico al actualizar 'executed_status' y registra el error.
    """
    error_message = await simulate_executed_error(task_id)
    if not error_message:
        raise HTTPException(status_code=404, detail="Task not found")

    raise HTTPException(status_code=500, detail=error_message)

@router.post("/{task_id}/simulate_state_error")
async def simulate_state_error_endpoint(task_id: int):
    """
    Simula un error específico al actualizar 'state' y registra el error.
    """
    error_message = await simulate_state_error(task_id)
    if not error_message:
        raise HTTPException(status_code=404, detail="Task not found")

    raise HTTPException(status_code=500, detail=error_message)