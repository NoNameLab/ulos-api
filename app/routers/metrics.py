from fastapi import APIRouter, HTTPException
from app.services.metrics import create_metric, get_metric, update_metric, delete_metric
from app.schemas.metrics import MetricCreate, metric_pydantic

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.post("/", response_model=metric_pydantic, status_code=201)
async def create_metric_endpoint(metric: MetricCreate):
    """
    Crea una nueva métrica en la base de datos.
    """
    return await create_metric(metric)


@router.get("/{metric_id}", response_model=metric_pydantic)
async def get_metric_endpoint(metric_id: int):
    """
    Recupera una métrica por su ID.
    """
    metric = await get_metric(metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric


@router.put("/{metric_id}", response_model=metric_pydantic)
async def update_metric_endpoint(metric_id: int, metric: MetricCreate):
    """
    Actualiza una métrica existente.
    """
    updated_metric = await update_metric(metric_id, metric)
    if not updated_metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return updated_metric


@router.delete("/{metric_id}", status_code=204)
async def delete_metric_endpoint(metric_id: int):
    """
    Elimina una métrica por su ID.
    """
    if not await delete_metric(metric_id):
        raise HTTPException(status_code=404, detail="Metric not found")
    return {"detail": "Metric deleted successfully"}