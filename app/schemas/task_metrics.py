from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.task_metrics import TaskMetrics

TaskMetricsPydantic = pydantic_model_creator(TaskMetrics, name="TaskMetrics")
TaskMetricsPydanticIn = pydantic_model_creator(TaskMetrics, name="TaskMetricsIn", exclude_readonly=True)

class TaskMetricsCreate(BaseModel):
    task_id: int
    requeue_count: int = Field(default=0, ge=0)
