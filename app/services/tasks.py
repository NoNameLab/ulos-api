from app.models.task import Task
from app.schemas.tasks import TaskCreate, TaskPydantic

async def create_task(task: TaskCreate):
    task_obj = await Task.create(**task.model_dump(exclude_unset=True))
    return await TaskPydantic.from_tortoise_orm(task_obj)

async def get_tasks():
    return await Task.all()
