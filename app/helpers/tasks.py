from app.models.task_execution_log import TaskExecutionLog

async def create_log_entry(task_id: int, step_name: str, old_state: int, new_state: int, error_message: str = None):
    await TaskExecutionLog.create(
        task_id=task_id,
        step_name=step_name,
        step_status=new_state,
        old_state=old_state,
        new_state=new_state,
        error_message=error_message
    )
