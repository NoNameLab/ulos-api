from app.models.metric import Metric
from app.schemas.metrics import MetricCreate, metric_pydantic


async def create_metric(metric: MetricCreate):
    metric_obj = await Metric.create(**metric.model_dump(exclude_unset=True))
    return await metric_pydantic.from_tortoise_orm(metric_obj)


async def get_metric(metric_id: int):
    return await Metric.get_or_none(id=metric_id)

async def update_metric(metric_id: int, metric: MetricCreate):
    metric_obj = await Metric.get_or_none(id=metric_id)
    if not metric_obj:
        return None
    await metric_obj.update_from_dict(metric.model_dump(exclude_unset=True)).save()
    return await metric_pydantic.from_tortoise_orm(metric_obj)

async def delete_metric(metric_id: int):
    deleted_count = await Metric.filter(id=metric_id).delete()
    return deleted_count > 0
