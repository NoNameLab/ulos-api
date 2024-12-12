# C:\Uuu\FastAPIULOS\routers\users_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, validator
from tortoise.contrib.pydantic import pydantic_model_creator
from models import User

router = APIRouter()

# Esquemas Pydantic para User
User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    role: str

    @validator("role")
    def validate_role(cls, value):
        if value not in {"student", "admin"}:
            raise ValueError("Role must be 'student' or 'admin'")
        return value

    @validator("email")
    def validate_email(cls, value):
        if not value.endswith("@uniandes.edu.co"):
            raise ValueError("Email must end with @uniandes.edu.co")
        return value


@router.post("/", response_model=User_Pydantic, status_code=201)
async def create_user(user: UserCreate):
    """
    Crea un nuevo usuario en la base de datos.
    """
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get("/{user_id}", response_model=User_Pydantic)
async def get_user(user_id: int):
    """
    Recupera un usuario por su ID.
    """
    user = await User.get_or_none(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await User_Pydantic.from_tortoise_orm(user)


@router.put("/{user_id}", response_model=User_Pydantic)
async def update_user(user_id: int, user: UserCreate):
    """
    Actualiza la información de un usuario existente.
    """
    user_obj = await User.get_or_none(user_id=user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    await user_obj.update_from_dict(user.dict(exclude_unset=True)).save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    """
    Elimina un usuario por su ID.
    """
    deleted_count = await User.filter(user_id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
