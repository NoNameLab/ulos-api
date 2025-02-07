from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.processing_stage import ProcessingStage
from app.schemas.processing_containers import ProcessingContainerRequest

ProcessingStagePydantic = pydantic_model_creator(ProcessingStage, name="ProcessingStage")
ProcessingStagePydanticIn = pydantic_model_creator(ProcessingStage, name="ProcessingStageIn", exclude_readonly=True)

class ProcessingStageRequest(BaseModel):
    stage_id: str | None
    stage_name: str
    stage_description: str
    container: ProcessingContainerRequest
    use_existing: bool

class ProcessingStageCreate(BaseModel):
    stage_name: str
    stage_description: str