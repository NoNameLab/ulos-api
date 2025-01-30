from fastapi import APIRouter, HTTPException
from app.services.users import create_user, get_user, update_user, delete_user
from app.schemas.users import UserCreate, user_pydantic

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=user_pydantic, status_code=201)
async def create_user_endpoint(user: UserCreate):
    """Crea un nuevo usuario."""
    return await create_user(user)

@router.get("/{user_id}", response_model=user_pydantic)
async def get_user_endpoint(user_id: int):
    """Recupera un usuario por su ID."""
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=user_pydantic)
async def update_user_endpoint(user_id: int, user: UserCreate):
    """Actualiza un usuario existente."""
    updated_user = await update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=204)
async def delete_user_endpoint(user_id: int):
    """Elimina un usuario por su ID."""
    if not await delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
