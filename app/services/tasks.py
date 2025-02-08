from app.models.task import Task


async def get_tasks():
    return await Task.all()
