
import json
import ftplib
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form

from app.auth.dependencies import RoleChecker
from app.models.processing_stage import ProcessingStage
from app.models.sysuser import RoleEnum, SysUser
from app.schemas.processing_containers import ProcessingContainerCreate
from app.schemas.processing_stages import ProcessingStageCreate
from app.schemas.stages_by_task_definitions import StageByTaskDefinitionCreate
from app.schemas.task_definitions import TaskDefinitionRequest, TaskDefinitionCreate
from app.services.processing_containers import create_processing_container
from app.services.processing_stages import create_processing_stage, get_processing_stage
from app.services.task_definitions import create_task_definition
from app.services.stages_by_task_definitions import create_stage_by_task_definition


router = APIRouter(prefix="/task-definitions", tags=["task_definitions"])

def upload_to_ftp(file: UploadFile) -> str:
    ftp_host = "localhost"
    ftp_user = "one"
    ftp_password = "123"
    ftp_directory = "/ftp/one/"

    try:
        with ftplib.FTP() as ftp:
            ftp.connect(ftp_host, 21)
            ftp.login(ftp_user, ftp_password)
            ftp.cwd(ftp_directory)

            server_filename = file.filename

            with file.file as f:
                ftp.storbinary(f"STOR {server_filename}", f)

            return f"{ftp_directory}{server_filename}"
    except ftplib.all_errors as e:
        raise HTTPException(status_code=500, detail=f"FTP error: {str(e)}")

@router.post("/")
async def create_task_definition_endpoint(
    task_definition: Annotated[str, Form()],
    files: list[UploadFile] = [],
    current_user: SysUser = Depends(RoleChecker([RoleEnum.PROFESSOR]))
):
    task_definition = json.loads(task_definition)

    task_definition = TaskDefinitionRequest(**task_definition)

    task_definition_db = TaskDefinitionCreate(
        type_name=task_definition.type_name,
        type_description=task_definition.type_description,
        created_by_id=current_user.id
    )

    # Create task definition and get its ID
    created_task_definition = await create_task_definition(task_definition_db)

    file_map = {file.filename: file for file in files} if files else {}

    for stage in task_definition.stages:
        if stage.use_existing == False:
            processing_stage_db = ProcessingStageCreate(
                stage_name=stage.stage_name,
                stage_description=stage.stage_description
            )

            # Create processing stage and get its ID
            created_processing_stage = await create_processing_stage(processing_stage_db)
        else:
            # If using existing stage, assume stage_id is provided
            created_processing_stage = await get_processing_stage(int(stage.stage_id))

        # Associate processing stage with task definition
        stage_by_task_definition_db = StageByTaskDefinitionCreate(
            task_definition_id=created_task_definition.id,
            processing_stage_id=created_processing_stage.id
        )

        await create_stage_by_task_definition(stage_by_task_definition_db)

        if stage.container.container_filename:
            file = file_map.get(stage.container.container_filename)
            if file:
                remote_path = upload_to_ftp(file)

                processing_container_db = ProcessingContainerCreate(
                    container_name=stage.container.container_name,
                    container_description=stage.container.container_description,
                    task_definition_id=created_task_definition.id,
                    processing_stage_id=created_processing_stage.id,
                    remote_storage_path=remote_path,
                    run_command=stage.container.run_command,
                    created_by_id=current_user.id
                )
                await create_processing_container(processing_container_db)

    return created_task_definition




