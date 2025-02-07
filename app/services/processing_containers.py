from app.models.processing_container import ProcessingContainer
from app.schemas.processing_containers import ProcessingContainerCreate, ProcessingContainerPydantic

async def create_processing_container(processing_container: ProcessingContainerCreate):
    processing_container_obj = await ProcessingContainer.create(**processing_container.model_dump(exclude_unset=True))
    return await ProcessingContainerPydantic.from_tortoise_orm(processing_container_obj)

async def get_processing_container(processing_stage_id: int):
    processing_container = await ProcessingContainer.get_or_none(processing_stage_id=processing_stage_id)
    return await ProcessingContainerPydantic.from_tortoise_orm(processing_container) if processing_container else None