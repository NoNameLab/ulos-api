from fastapi import HTTPException
from app.models.assignment import Assignment
from app.models.task import Task
from app.schemas.assignments import AssignmentCreate, AssignmentPydantic


async def create_assignment(assignment: AssignmentCreate):
    assignment_obj = await Assignment.create(**assignment.model_dump(exclude_unset=True))
    return await AssignmentPydantic.from_tortoise_orm(assignment_obj)


async def get_assignment(assignment_id: int):
    assignment = await Assignment.get_or_none(id=assignment_id)
    return await AssignmentPydantic.from_tortoise_orm(assignment) if assignment else None


async def update_assignment(assignment_id: int, assignment: AssignmentCreate):
    assignment_obj = await Assignment.get_or_none(id=assignment_id).prefetch_related("tasks")

    if not assignment_obj:
        return None

    tasks_count = await Task.filter(assignment_id=assignment_id).count()
    if tasks_count > 0:
        raise HTTPException(status_code=400, detail="No se puede actualizar la tarea porque ya tiene envíos relacionados.")

    await assignment_obj.update_from_dict(assignment.model_dump(exclude_unset=True)).save()
    return await AssignmentPydantic.from_tortoise_orm(assignment_obj)


async def delete_assignment(assignment_id: int):
    deleted_count = await Assignment.filter(id=assignment_id).delete()
    return deleted_count > 0


async def get_assignments_by_course(course_id: int):
    assignments = Assignment.filter(course_id=course_id).prefetch_related("task_definition")
    return await AssignmentPydantic.from_queryset(assignments)