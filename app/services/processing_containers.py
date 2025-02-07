from app.models.processing_container import ProcessingContainer
from app.schemas.processing_containers import ProcessingContainerCreate, ProcessingContainerPydantic

async def create_processing_container(processing_container: ProcessingContainerCreate):
    processing_container_obj = await ProcessingContainer.create(**processing_container.model_dump(exclude_unset=True))
    return await ProcessingContainerPydantic.from_tortoise_orm(processing_container_obj)