from tortoise import fields
from tortoise.models import Model

class Assignment(Model):
    id = fields.IntField(pk=True)
    course = fields.ForeignKeyField("models.Course", related_name="assignments")
    task_definition = fields.ForeignKeyField("models.TaskDefinition", related_name="assignments")
    assignment_name = fields.CharField(max_length=255)
    assignment_description = fields.TextField()
    assignment_start_date = fields.DatetimeField(null=True)
    assignment_end_date = fields.DatetimeField(null=True)
    created_by = fields.ForeignKeyField("models.SysUser", related_name="created_assignments")
    creation_timestamp = fields.DatetimeField(auto_now_add=True)