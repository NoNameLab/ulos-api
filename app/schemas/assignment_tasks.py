from pydantic import BaseModel


class StudentTaskStatus(BaseModel):
    student_id: int
    student_email: str
    parsing_status: str
    execution_status: str
