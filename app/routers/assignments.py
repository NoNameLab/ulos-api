from fastapi import APIRouter, Depends, UploadFile

from app.auth.dependencies import RoleChecker
from app.helpers.ftp_utils import upload_to_ftp
from app.models.sysuser import RoleEnum, SysUser
from app.schemas.tasks import TaskCreate
from app.services.tasks import create_task


router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.post("/{assignment_id}/submit")
async def submit_assignment_endpoint(assignment_id: int, file: UploadFile, current_user: SysUser = Depends(RoleChecker([RoleEnum.STUDENT]))):
    remote_storage_path = upload_to_ftp(file)

    task = TaskCreate(assignment_id=assignment_id, remote_storage_path=remote_storage_path, created_by_id=current_user.id)

    return await create_task(task)