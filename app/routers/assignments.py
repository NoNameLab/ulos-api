from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile

from app.auth.dependencies import RoleChecker
from app.helpers.ftp_utils import upload_to_ftp
from app.helpers.rabbitmq_utils import publish_to_rabbitmq
from app.models.course_user import RoleEnum
from app.models.sysuser import SysUser
from app.schemas.assignment_tasks import StudentTaskStatus
from app.schemas.assignments import AssignmentCreate, AssignmentRequest
from app.schemas.task_metrics import TaskMetricsCreate
from app.schemas.task_stage_statuses import TaskStageStatusCreate
from app.schemas.tasks import TaskCreate
from app.services.assignment_tasks import get_assignment_tasks_statuses
from app.services.assignments import delete_assignment, get_assignment, update_assignment
from app.services.stages_by_task_definitions import get_stages_by_task_definition
from app.services.task_metrics import create_task_metrics
from app.services.task_stage_statuses import create_task_stage_status
from app.services.tasks import create_task


router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.post("/{assignment_id}/submit")
async def submit_assignment_endpoint(assignment_id: int, file: UploadFile, current_user: SysUser = Depends(RoleChecker([RoleEnum.STUDENT]))):
    remote_storage_path = upload_to_ftp(file)

    task = TaskCreate(assignment_id=assignment_id,
                      remote_storage_path=remote_storage_path, created_by_id=current_user.id)

    task = await create_task(task)

    task_metrics = TaskMetricsCreate(task_id=task.id)

    await create_task_metrics(task_metrics)

    assignment = await get_assignment(assignment_id)

    stages = await get_stages_by_task_definition(assignment.task_definition.id)

    for stage in stages:
        task_stage_status = TaskStageStatusCreate(
            task_id=task.id, processing_stage_id=stage.id)

        await create_task_stage_status(task_stage_status)

    stages_info = [
        [
            stage.stage_name,
            stage.container.remote_storage_path,
            stage.container.run_command
        ]
        for stage in stages
    ]
    task_definition_payload = {
        "definitionName": assignment.task_definition.definition_name,
        "stages": stages_info
    }

    publish_to_rabbitmq(
        task_id=task.id,
        user_id=current_user.id,
        remote_storage_path=remote_storage_path,
        task_definition=task_definition_payload
    )

    return task


@router.get("/{assignment_id}")
async def get_assignment_endpoint(assignment_id: int):
    assignment = await get_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


@router.put("/{assignment_id}")
async def update_assignment_endpoint(
    assignment_id: int,
    assignment: AssignmentRequest,
    current_user: SysUser = Depends(RoleChecker([RoleEnum.PROFESSOR]))
):
    existing = await get_assignment(assignment_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Assignment not found")

    assignment_data = AssignmentCreate(
        course_id=existing.course.id,
        created_by_id=current_user.id,
        **assignment.dict()
    )

    updated_assignment = await update_assignment(assignment_id, assignment_data)

    if not updated_assignment:
        raise HTTPException(status_code=400, detail="No se puede actualizar la tarea porque ya tiene envíos.")

    return updated_assignment


@router.delete("/{assignment_id}", status_code=204)
async def delete_assignment_endpoint(assignment_id: int, current_user: SysUser = Depends(RoleChecker([RoleEnum.PROFESSOR]))):
    deleted = await delete_assignment(assignment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return {"detail": "Assignment deleted successfully"}


@router.get(
    "/{assignment_id}/tasks",
    response_model=List[StudentTaskStatus],
    summary="Obtener estados de parsing y execution por estudiante"
)
async def list_assignment_tasks(
    assignment_id: int = Path(..., description="ID de la asignación")
):
    return await get_assignment_tasks_statuses(assignment_id)
