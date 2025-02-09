from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.processing_status import ProcessingStatus

ProcessingStatusPydantic = pydantic_model_creator(ProcessingStatus, name="ProcessingStatus")
ProcessingStatusPydanticIn = pydantic_model_creator(ProcessingStatus, name="ProcessingStatusIn", exclude_readonly=True)

class ProcessingStatusCreate(BaseModel):
    status_name: str
    status_description: str