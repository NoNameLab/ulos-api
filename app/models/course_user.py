from tortoise import fields
from tortoise.models import Model
from enum import Enum


class RoleEnum(str, Enum):
    ASSISTANT = 'assistant'
    PROFESSOR = 'professor'
    STUDENT = 'student'


class CourseUser(Model):
    id = fields.IntField(pk=True)
    course = fields.ForeignKeyField("models.Course", related_name="users")
    user = fields.ForeignKeyField("models.SysUser", related_name="courses")
    course_role = fields.CharEnumField(RoleEnum)

    class Meta:
        unique_together = ("course", "user")
