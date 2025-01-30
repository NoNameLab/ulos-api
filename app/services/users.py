from app.models.user import User
from app.schemas.users import UserCreate, user_pydantic

async def create_user(user: UserCreate):
    """Crea un nuevo usuario."""
    user_obj = await User.create(**user.model_dump(exclude_unset=True))
    return await user_pydantic.from_tortoise_orm(user_obj)

async def get_user(user_id: int):
    """Recupera un usuario por su ID."""
    user = await User.get_or_none(id=user_id)
    return await user_pydantic.from_tortoise_orm(user) if user else None

async def update_user(user_id: int, user: UserCreate):
    """Actualiza un usuario existente."""
    user_obj = await User.get_or_none(id=user_id)
    if not user_obj:
        return None
    await user_obj.update_from_dict(user.model_dump(exclude_unset=True)).save()
    return await user_pydantic.from_tortoise_orm(user_obj)

async def delete_user(user_id: int) -> bool:
    """Elimina un usuario por su ID."""
    deleted_count = await User.filter(id=user_id).delete()
    return deleted_count > 0