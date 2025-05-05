from app.models.processing_stage import ProcessingStage
from app.schemas.processing_stages import ProcessingStageCreate, ProcessingStagePydantic


async def create_processing_stage(processing_stage: ProcessingStageCreate):
    processing_stage_obj = await ProcessingStage.create(**processing_stage.model_dump(exclude_unset=True))
    return await ProcessingStagePydantic.from_tortoise_orm(processing_stage_obj)


async def get_processing_stage(processing_stage_id: int):
    processing_stage = await ProcessingStage.get_or_none(id=processing_stage_id)
    return await ProcessingStagePydantic.from_tortoise_orm(processing_stage) if processing_stage else None


async def get_processing_stage_by_name(processing_stage_name: str):
    processing_stage = await ProcessingStage.get_or_none(stage_name=processing_stage_name)
    return processing_stage
