from app.models.task_metrics import TaskMetrics
from app.schemas.task_metrics import TaskMetricsCreate, TaskMetricsPydantic


async def create_task_metrics(task_metrics: TaskMetricsCreate):
    task_metric_obj = await TaskMetrics.create(**task_metrics.model_dump(exclude_unset=True))
    return await TaskMetricsPydantic.from_tortoise_orm(task_metric_obj)