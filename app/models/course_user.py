from tortoise import fields
from tortoise.models import Model


class CourseUser(Model):
    id = fields.IntField(pk=True)
    course = fields.ForeignKeyField("models.Course", related_name="users")
    user = fields.ForeignKeyField("models.SysUser", related_name="courses")

    class Meta:
        unique_together = ("course", "user")
