from app.models.file import File
from app.schemas.files import FileCreate, file_pydantic


async def create_file(file: FileCreate):
    file_obj = await File.create(**file.model_dump(exclude_unset=True))
    return await file_pydantic.from_tortoise_orm(file_obj)

async def get_file(file_id: int):
    file = await File.get_or_none(id=file_id)
    return await file_pydantic.from_tortoise_orm(file) if file else None

async def update_file(file_id: int, file: FileCreate):
    file_obj = await File.get_or_none(id=file_id)
    if not file_obj:
        return None
    await file_obj.update_from_dict(file.model_dump(exclude_unset=True)).save()
    return await file_pydantic.from_tortoise_orm(file_obj)

async def delete_file(file_id: int) -> bool:
    deleted_count = await File.filter(id=file_id).delete()
    return deleted_count > 0
