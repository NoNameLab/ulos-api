from app.models.assignment import Assignment
from app.schemas.assignments import AssignmentCreate, AssignmentPydantic


async def create_assignment(assignment: AssignmentCreate):
    assignment_obj = await Assignment.create(**assignment.model_dump(exclude_unset=True))
    return await AssignmentPydantic.from_tortoise_orm(assignment_obj)


async def get_assignment(assignment_id: int):
    assignment = await Assignment.get_or_none(id=assignment_id)
    return await AssignmentPydantic.from_tortoise_orm(assignment) if assignment else None


async def update_assignment(assignment_id: int, assignment: AssignmentCreate):
    assignment_obj = await Assignment.get_or_none(id=assignment_id)
    if not assignment_obj:
        return None
    await assignment_obj.update_from_dict(assignment.model_dump(exclude_unset=True)).save()
    return await AssignmentPydantic.from_tortoise_orm(assignment_obj)


async def delete_assignment(assignment_id: int):
    deleted_count = await Assignment.filter(id=assignment_id).delete()
    return deleted_count > 0