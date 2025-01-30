from fastapi import APIRouter, HTTPException
from app.services.task_types import create_task_type, get_task_type, update_task_type, delete_task_type
from app.schemas.task_types import TaskTypeCreate, taskType_pydantic

router = APIRouter(prefix="/task_types", tags=["TaskTypes"])

@router.post("/", response_model=taskType_pydantic, status_code=201)
async def create_task_type_route_endpoint(task_type: TaskTypeCreate):
    """Crea un nuevo tipo de tarea."""
    return await create_task_type(task_type)

@router.get("/{task_type_id}", response_model=taskType_pydantic)
async def get_task_type_route_endpoint(task_type_id: int):
    """Recupera un tipo de tarea por su ID."""
    task_type = await get_task_type(task_type_id)
    if not task_type:
        raise HTTPException(status_code=404, detail="Task type not found")
    return task_type

@router.put("/{task_type_id}", response_model=taskType_pydantic)
async def update_task_type_route_endpoint(task_type_id: int, task_type: TaskTypeCreate):
    """Actualiza un tipo de tarea existente."""
    updated_task_type = await update_task_type(task_type_id, task_type)
    if not updated_task_type:
        raise HTTPException(status_code=404, detail="Task type not found")
    return updated_task_type

@router.delete("/{task_type_id}", status_code=204)
async def delete_task_type_route_endpoint(task_type_id: int):
    """Elimina un tipo de tarea por su ID."""
    if not await delete_task_type(task_type_id):
        raise HTTPException(status_code=404, detail="Task type not found")
    return {"detail": "Task type deleted successfully"}
