from pydantic import BaseModel, condecimal
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.metric import Metric

# Esquemas Pydantic
metric_pydantic = pydantic_model_creator(Metric, name="Metric")
metric_pydanticIn = pydantic_model_creator(Metric, name="MetricIn", exclude_readonly=True)

# Esquema para crear una métrica
class MetricCreate(BaseModel):
    task_id: int
    execution_time: condecimal(max_digits=10, decimal_places=2) = None # type: ignore
    machine_id: int = None
    objective_metric: condecimal(max_digits=10, decimal_places=2) = None # type: ignore
