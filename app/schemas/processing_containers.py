from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.processing_container import ProcessingContainer

ProcessingContainerPydantic = pydantic_model_creator(ProcessingContainer, name="ProcessingContainer")
ProcessingContainerPydanticIn = pydantic_model_creator(ProcessingContainer, name="ProcessingContainerIn", exclude_readonly=True)

class ProcessingContainerRequest(BaseModel):
    container_name: str
    container_description: str
    run_command: str
    container_filename: str

class ProcessingContainerCreate(BaseModel):
    container_name: str
    container_description: str
    task_definition_id: int
    processing_stage_id: int
    remote_storage_path: str
    run_command: str
    created_by_id: int
