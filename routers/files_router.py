# C:\Uuu\FastAPIULOS\routers\files_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from models import File

router = APIRouter()

# Esquemas Pydantic para File
File_Pydantic = pydantic_model_creator(File, name="File")
FileIn_Pydantic = pydantic_model_creator(File, name="FileIn", exclude_readonly=True)

class FileCreate(BaseModel):
    task_id: int
    file_name: str = None
    file_path: str = None


@router.post("/", response_model=File_Pydantic, status_code=201)
async def create_file(file: FileCreate):
    """
    Crea un nuevo archivo en la base de datos.
    """
    file_obj = await File.create(**file.dict(exclude_unset=True))
    return await File_Pydantic.from_tortoise_orm(file_obj)


@router.get("/{file_id}", response_model=File_Pydantic)
async def get_file(file_id: int):
    """
    Recupera un archivo por su ID.
    """
    file = await File.get_or_none(file_id=file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return await File_Pydantic.from_tortoise_orm(file)


@router.put("/{file_id}", response_model=File_Pydantic)
async def update_file(file_id: int, file: FileCreate):
    """
    Actualiza un archivo existente.
    """
    file_obj = await File.get_or_none(file_id=file_id)
    if not file_obj:
        raise HTTPException(status_code=404, detail="File not found")
    await file_obj.update_from_dict(file.dict(exclude_unset=True)).save()
    return await File_Pydantic.from_tortoise_orm(file_obj)


@router.delete("/{file_id}", status_code=204)
async def delete_file(file_id: int):
    """
    Elimina un archivo por su ID.
    """
    deleted_count = await File.filter(file_id=file_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="File not found")
    return {"detail": "File deleted successfully"}
