from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.file import File

# Esquemas de Pydantic
file_pydantic = pydantic_model_creator(File, name="File")
file_pydanticIn = pydantic_model_creator(File, name="FileIn", exclude_readonly=True)

# Esquema para crear un archivo
class FileCreate(BaseModel):
    task_id: int
    name: str | None = None
    path: str | None = None
