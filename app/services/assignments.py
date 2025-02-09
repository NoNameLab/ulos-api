from app.models.assignment import Assignment
from app.schemas.assignments import AssignmentPydantic


async def get_assignment(assignment_id: int):
    assignment = await Assignment.get_or_none(id=assignment_id)
    return await AssignmentPydantic.from_tortoise_orm(assignment) if assignment else None