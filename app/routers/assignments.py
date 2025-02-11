from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.auth.dependencies import RoleChecker
from app.helpers.ftp_utils import upload_to_ftp
from app.helpers.rabbitmq_utils import publish_to_rabbitmq
from app.models.sysuser import RoleEnum, SysUser
from app.schemas.assignments import AssignmentCreate
from app.schemas.task_metrics import TaskMetricsCreate
from app.schemas.task_stage_statuses import TaskStageStatusCreate
from app.schemas.tasks import TaskCreate
from app.services.assignments import delete_assignment, get_assignment, update_assignment
from app.services.stages_by_task_definitions import get_stages_by_task_definition
from app.services.task_metrics import create_task_metrics
from app.services.task_stage_statuses import create_task_stage_status
from app.services.tasks import create_task


router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.post("/{assignment_id}/submit")
async def submit_assignment_endpoint(assignment_id: int, file: UploadFile, current_user: SysUser = Depends(RoleChecker([RoleEnum.STUDENT]))):
    remote_storage_path = upload_to_ftp(file)

    task = TaskCreate(assignment_id=assignment_id, remote_storage_path=remote_storage_path, created_by_id=current_user.id)

    task = await create_task(task)

    task_metrics = TaskMetricsCreate(task_id=task.id)

    await create_task_metrics(task_metrics)

    assignment = await get_assignment(assignment_id)

    stages = await get_stages_by_task_definition(assignment.task_definition.id)

    for stage in stages:
        task_stage_status = TaskStageStatusCreate(task_id=task.id, processing_stage_id=stage.id)

        await create_task_stage_status(task_stage_status)

    stages_names = [stage.stage_name for stage in stages]

    container_images_paths = [stage.container.remote_storage_path for stage in stages]

    publish_to_rabbitmq(task.id, current_user.id, assignment.task_definition.definition_name, remote_storage_path, container_images_paths, stages_names)


    return task


@router.put("/{assignment_id}")
async def update_assignment_endpoint(assignment_id: int, assignment: AssignmentCreate, current_user: SysUser = Depends(RoleChecker([RoleEnum.PROFESSOR]))):
    updated_assignment = await update_assignment(assignment_id, assignment)
    if not updated_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return updated_assignment


@router.delete("/{assignment_id}", status_code=204)
async def delete_assignment_endpoint(assignment_id: int, current_user: SysUser = Depends(RoleChecker([RoleEnum.PROFESSOR]))):
    deleted = await delete_assignment(assignment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return {"detail": "Assignment deleted successfully"}