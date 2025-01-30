from fastapi import APIRouter, HTTPException
from app.schemas.files import FileCreate, file_pydantic
from app.services.files import create_file, get_file, update_file, delete_file

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/", response_model=file_pydantic, status_code=201)
async def create_file_endpoint(file: FileCreate):
    """
    Crea un nuevo archivo en la base de datos.
    """
    return await create_file(file)

@router.get("/{file_id}", response_model=file_pydantic)
async def get_file_endpoint(file_id: int):
    """
    Recupera un archivo por su ID.
    """
    file = await get_file(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file

@router.put("/{file_id}", response_model=file_pydantic)
async def update_file_endpoint(file_id: int, file: FileCreate):
    """
    Actualiza un archivo existente.
    """
    updated_file = await update_file(file_id, file)
    if not updated_file:
        raise HTTPException(status_code=404, detail="File not found")
    return updated_file

@router.delete("/{file_id}", status_code=204)
async def delete_file_endpoint(file_id: int):
    """
    Elimina un archivo por su ID.
    """
    if not await delete_file(file_id):
        raise HTTPException(status_code=404, detail="File not found")
    return {"detail": "File deleted successfully"}
