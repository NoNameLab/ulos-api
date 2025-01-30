from app.models.task import Task

from app.schemas.tasks import StatusUpdate, TaskCreate, task_pydantic
from app.helpers.tasks import create_log_entry

STATE_NAMES = {
    0: "Pending",
    1: "In Progress",
    2: "Completed",
    3: "Failed"
}

async def create_task(task: TaskCreate):
    task_obj = await Task.create(**task.model_dump(exclude_unset=True))
    return await task_pydantic.from_tortoise_orm(task_obj)

async def get_task(task_id: int):
    task = await Task.get_or_none(id=task_id)
    return await task_pydantic.from_tortoise_orm(task) if task else None

async def update_task(task_id: int, task: TaskCreate):
    task_obj = await Task.get_or_none(id=task_id)
    if not task_obj:
        return None
    await task_obj.update_from_dict(task.model_dump(exclude_unset=True)).save()
    return await task_pydantic.from_tortoise_orm(task_obj)

async def delete_task(task_id: int):
    deleted_count = await Task.filter(id=task_id).delete()
    return deleted_count > 0

async def update_parsed_status(task_id: int, status_update: StatusUpdate):
    task_obj = await Task.get_or_none(id=task_id)
    if not task_obj:
        return None
    old_status = task_obj.parsed_status
    task_obj.parsed_status = status_update.status
    await task_obj.save()

    await create_log_entry(task_id, step_name = "Parsing Status Update", old_state=old_status, new_state=task_obj.parsed_status)
    return await task_pydantic.from_tortoise_orm(task_obj)

async def update_executed_status(task_id: int, status_update: StatusUpdate):
    task = await Task.get_or_none(id=task_id)
    if not task:
        return None
    old_status = task.executed_status
    task.executed_status = status_update.status
    await task.save()
    await create_log_entry(task_id, step_name="Execution Status Update",old_state=old_status, new_state=task.executed_status)
    return await task_pydantic.from_tortoise_orm(task)

async def update_state(task_id: int, status_update: StatusUpdate):
    task = await Task.get_or_none(id=task_id)
    if not task:
        raise None
    old_status = task.state
    task.state = status_update.status
    await task.save()
    await create_log_entry(task_id, step_name="Status Update",old_state=old_status, new_state=task.state)
    return await task_pydantic.from_tortoise_orm(task)


async def group_tasks_by_state():
    tasks = await Task.all()
    grouped_tasks = {
        "pending": [task.task_id for task in tasks if task.state == 0],
        "in_progress": [task.task_id for task in tasks if task.state == 1],
        "completed": [task.task_id for task in tasks if task.state == 2],
        "failed": [task.task_id for task in tasks if task.state == 3],
    }
    return grouped_tasks

async def filter_tasks_by_state(state: int):
    tasks = await Task.filter(state=state).values("task_id", "file_name", "state")
    return tasks

async def get_task_states():
    return STATE_NAMES

async def get_tasks_with_state_names():
    tasks = await Task.all().values("task_id", "file_name", "state")
    tasks_with_names = [
        {
            "task_id": task["task_id"],
            "file_name": task["file_name"],
            "state": STATE_NAMES.get(task["state"], "Unknown")
        }
        for task in tasks
    ]
    return tasks_with_names

async def simulate_parsed_error(task_id: int):
    task = await Task.get_or_none(id=task_id)
    if not task:
        return None

    old_status = task.parsed_status
    error_message = "Unexpected error occurred while updating parsed status."

    # Simular siempre un error específico
    await create_log_entry(task_id, step_name="Parsing Error", old_state=old_status, new_state=3, error_message=error_message)

    return error_message

async def simulate_executed_error(task_id: int):
    task = await Task.get_or_none(id=task_id)
    if not task:
        return None

    old_status = task.executed_status
    error_message = "Unexpected error occurred while updating executed status."

    # Crear un registro de error en los logs
    await create_log_entry(task_id, step_name="Execution Error", old_state=old_status, new_state=3, error_message=error_message)

    return error_message


async def simulate_state_error(task_id: int):
    task = await Task.get_or_none(id=task_id)
    if not task:
        return None

    old_status = task.state
    error_message = "Unexpected error occurred while updating task state."

    # Crear un registro de error en los logs
    await create_log_entry(task_id, old_state=old_status, new_state=3, error_message=error_message)

    return error_message