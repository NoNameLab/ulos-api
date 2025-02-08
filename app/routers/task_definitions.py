
import json
import ftplib
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form

from app.auth.dependencies import RoleChecker
from app.helpers.ftp_utils import upload_to_ftp
from app.models.processing_stage import ProcessingStage
from app.models.sysuser import RoleEnum, SysUser
from app.models.task_definition import TaskDefinition
from app.schemas.processing_containers import ProcessingContainerCreate
from app.schemas.processing_stages import ProcessingStageCreate
from app.schemas.stages_by_task_definitions import StageByTaskDefinitionCreate
from app.schemas.task_definitions import TaskDefinitionRequest, TaskDefinitionCreate
from app.services.processing_containers import create_processing_container, get_processing_container
from app.services.processing_stages import create_processing_stage, get_processing_stage
from app.services.task_definitions import create_task_definition, get_task_definitions
from app.services.stages_by_task_definitions import create_stage_by_task_definition


router = APIRouter(prefix="/task-definitions", tags=["task_definitions"])


@router.post("/")
async def create_task_definition_endpoint(
    task_definition: Annotated[str, Form()],
    files: list[UploadFile] = [],
    current_user: SysUser = Depends(RoleChecker([RoleEnum.PROFESSOR]))
):
    task_definition = json.loads(task_definition)

    task_definition = TaskDefinitionRequest(**task_definition)

    task_definition_db = TaskDefinitionCreate(
        definition_name=task_definition.definition_name,
        definition_description=task_definition.definition_description,
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


@router.get("/")
async def get_task_definitions_endpoint(current_user: SysUser = Depends(RoleChecker([RoleEnum.PROFESSOR]))):
    task_definitions = await get_task_definitions()
    results = []
    for task in task_definitions:
        task_dict = {
            "id": task.id,
            "definition_name": task.definition_name,
            "definition_description": task.definition_description,
            "stages": []
        }
        for stage_by_task in task.stages:
            stage = stage_by_task.processing_stage
            stage_dict = {
                "stage_name": stage.stage_name,
                "stage_description": stage.stage_description,
                "container": {
                    "container_name": stage.container.container_name,
                    "container_description": stage.container.container_description,
                    "remote_storage_path": stage.container.remote_storage_path,
                    "run_command": stage.container.run_command
                }
            }
            task_dict["stages"].append(stage_dict)
        results.append(task_dict)
    return results




