# C:\Uuu\FastAPIULOS\routers\task_types_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from models import TaskType

router = APIRouter()

# Esquemas Pydantic para TaskType
TaskType_Pydantic = pydantic_model_creator(TaskType, name="TaskType")
TaskTypeIn_Pydantic = pydantic_model_creator(TaskType, name="TaskTypeIn", exclude_readonly=True)

class TaskTypeCreate(BaseModel):
    task_type_name: str

    @staticmethod
    def validate_task_type_name(value: str):
        if len(value.strip()) == 0:
            raise ValueError("Task type name cannot be empty")
        return value


@router.post("/", response_model=TaskType_Pydantic, status_code=201)
async def create_task_type(task_type: TaskTypeCreate):
    """
    Crea un nuevo tipo de tarea en la base de datos.
    """
    task_type_obj = await TaskType.create(**task_type.dict(exclude_unset=True))
    return await TaskType_Pydantic.from_tortoise_orm(task_type_obj)


@router.get("/{task_type_id}", response_model=TaskType_Pydantic)
async def get_task_type(task_type_id: int):
    """
    Recupera un tipo de tarea por su ID.
    """
    task_type = await TaskType.get_or_none(task_type_id=task_type_id)
    if not task_type:
        raise HTTPException(status_code=404, detail="Task type not found")
    return await TaskType_Pydantic.from_tortoise_orm(task_type)


@router.put("/{task_type_id}", response_model=TaskType_Pydantic)
async def update_task_type(task_type_id: int, task_type: TaskTypeCreate):
    """
    Actualiza un tipo de tarea existente.
    """
    task_type_obj = await TaskType.get_or_none(task_type_id=task_type_id)
    if not task_type_obj:
        raise HTTPException(status_code=404, detail="Task type not found")
    await task_type_obj.update_from_dict(task_type.dict(exclude_unset=True)).save()
    return await TaskType_Pydantic.from_tortoise_orm(task_type_obj)


@router.delete("/{task_type_id}", status_code=204)
async def delete_task_type(task_type_id: int):
    """
    Elimina un tipo de tarea por su ID.
    """
    deleted_count = await TaskType.filter(task_type_id=task_type_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Task type not found")
    return {"detail": "Task type deleted successfully"}
