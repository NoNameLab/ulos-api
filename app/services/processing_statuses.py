from app.models.processing_status import ProcessingStatus
from app.schemas.processing_statuses import ProcessingStatusPydantic


async def get_processing_status(processing_status_id: int):
    processing_status = await ProcessingStatus.get_or_none(id=processing_status_id)
    return await ProcessingStatusPydantic.from_tortoise_orm(processing_status) if processing_status else None