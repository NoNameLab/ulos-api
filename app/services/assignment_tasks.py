from typing import List, Optional
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException

from ..models.assignment import Assignment
from ..models.course_user import CourseUser, RoleEnum
from ..models.task import Task
from ..models.processing_stage import ProcessingStage
from ..models.task_stage_status import TaskStageStatus
from ..schemas.assignment_tasks import StudentTaskStatus


async def get_assignment_tasks_statuses(assignment_id: int) -> List[StudentTaskStatus]:
    # 1. Validar existencia de la asignación
    try:
        assignment = await Assignment.get(id=assignment_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # 2. Obtener los estudiantes del curso de esa asignación
    students = await CourseUser.filter(
        course_id=assignment.course_id,
        course_role=RoleEnum.STUDENT
    ).prefetch_related("user")

    # 3. Cargar los dos stages fijos (aquí por ID o por nombre)
    parsing_stage   = await ProcessingStage.get(id=1)
    execution_stage = await ProcessingStage.get(id=2)

    results: List[StudentTaskStatus] = []

    async def _get_status(task_id: int, stage_id: int) -> str:
        """
        Retorna el status_name del TaskStageStatus para el task y stage dados,
        o "not_started" si no existe.
        """
        tss = await TaskStageStatus.filter(
            task_id=task_id,
            processing_stage_id=stage_id
        ).select_related("processing_status").first()

        if not tss:
            return "not_started"
        return tss.processing_status.status_name

    for cu in students:
        # 4. Buscar la tarea (Task) de este estudiante en la asignación
        task: Optional[Task] = await Task.filter(
            assignment_id=assignment_id,
            created_by_id=cu.user_id
        ).first()

        if not task:
            parsing_status = execution_status = "not_submitted"
        else:
            parsing_status   = await _get_status(task.id, parsing_stage.id)
            execution_status = await _get_status(task.id, execution_stage.id)

        results.append(StudentTaskStatus(
            student_id       = cu.user.id,
            student_email     = cu.user.email,
            parsing_status   = parsing_status,
            execution_status = execution_status
        ))

    return results
