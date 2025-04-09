from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth.dependencies import RoleChecker
from app.models.course_user import RoleEnum
from app.models.sysuser import SysUser
from app.models.task import Task
from app.schemas.task_logs import TaskLogCreate, TaskLogPydantic, TaskLogRequest
from app.schemas.task_metrics import TaskMetricsPydantic
from app.schemas.tasks import TaskPydantic
from app.services.task_logs import create_task_log
from app.services.task_metrics import requeue_task
from app.services.tasks import get_task, get_task_by_assignment_and_user, get_tasks, update_task



router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskPydantic])
async def get_tasks_endpoint():
    return await get_tasks()

@router.get("/{task_id}", response_model=TaskPydantic)
async def get_task_endpoint(task_id: int):
    return await get_task(task_id)

@router.get("", response_model=Optional[TaskPydantic])
async def get_task_by_assignment_and_user_endpoint(
    assignment_id: int = Query(...),
    current_user: SysUser = Depends(RoleChecker([RoleEnum.STUDENT]))
):
    task = await get_task_by_assignment_and_user(assignment_id, current_user.id)
    return task


@router.patch("/{task_id}", response_model=TaskPydantic)
async def update_task_endpoint(task_id: int, stage_status_updates: dict):
    try:
        return await update_task(task_id, stage_status_updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{task_id}/requeue", response_model=TaskMetricsPydantic)
async def requeue_task_endpoint(task_id: int):
    return await requeue_task(task_id)

@router.post("/{task_id}/logs", response_model=TaskLogPydantic)
async def create_task_log_endpoint(task_id: int, task_log: TaskLogRequest):
    task_log = TaskLogCreate(task_id=task_id, log_message=task_log.log_message)
    return await create_task_log(task_log)