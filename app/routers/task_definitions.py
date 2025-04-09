
from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import RoleChecker
from app.models.course_user import RoleEnum
from app.models.sysuser import SysUser
from app.services.task_definitions import get_task_definitions, get_task_definition


router = APIRouter(prefix="/task-definitions", tags=["task_definitions"])


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


@router.get("/{task_definition_id}")
async def get_task_definition_endpoint(task_definition_id: int, current_user: SysUser = Depends(RoleChecker([RoleEnum.PROFESSOR]))):
    task_definition = await get_task_definition(task_definition_id)

    if not task_definition:
        raise HTTPException(
            status_code=404, detail="Task definition not found")

    task_dict = {
        "id": task_definition.id,
        "definition_name": task_definition.definition_name,
        "definition_description": task_definition.definition_description,
        "stages": []
    }

    for stage_by_task in task_definition.stages:
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

    return task_dict
