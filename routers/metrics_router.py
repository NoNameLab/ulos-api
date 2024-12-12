# C:\Uuu\FastAPIULOS\routers\metrics_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, condecimal
from tortoise.contrib.pydantic import pydantic_model_creator
from models import Metric

router = APIRouter()

# Esquemas Pydantic para Metric
Metric_Pydantic = pydantic_model_creator(Metric, name="Metric")
MetricIn_Pydantic = pydantic_model_creator(Metric, name="MetricIn", exclude_readonly=True)

class MetricCreate(BaseModel):
    task_id: int
    execution_time: condecimal(max_digits=10, decimal_places=2) = None # type: ignore
    machine_id: int = None
    objective_metric: condecimal(max_digits=10, decimal_places=2) = None # type: ignore


@router.post("/", response_model=Metric_Pydantic, status_code=201)
async def create_metric(metric: MetricCreate):
    """
    Crea una nueva métrica en la base de datos.
    """
    metric_obj = await Metric.create(**metric.dict(exclude_unset=True))
    return await Metric_Pydantic.from_tortoise_orm(metric_obj)


@router.get("/{metric_id}", response_model=Metric_Pydantic)
async def get_metric(metric_id: int):
    """
    Recupera una métrica por su ID.
    """
    metric = await Metric.get_or_none(metric_id=metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return await Metric_Pydantic.from_tortoise_orm(metric)


@router.put("/{metric_id}", response_model=Metric_Pydantic)
async def update_metric(metric_id: int, metric: MetricCreate):
    """
    Actualiza una métrica existente.
    """
    metric_obj = await Metric.get_or_none(metric_id=metric_id)
    if not metric_obj:
        raise HTTPException(status_code=404, detail="Metric not found")
    await metric_obj.update_from_dict(metric.dict(exclude_unset=True)).save()
    return await Metric_Pydantic.from_tortoise_orm(metric_obj)


@router.delete("/{metric_id}", status_code=204)
async def delete_metric(metric_id: int):
    """
    Elimina una métrica por su ID.
    """
    deleted_count = await Metric.filter(metric_id=metric_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Metric not found")
    return {"detail": "Metric deleted successfully"}
