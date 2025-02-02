from tortoise import fields
from tortoise.models import Model

class Task(Model):
    id = fields.BigIntField(pk=True)
    assignment = fields.ForeignKeyField("models.Assignment", related_name="tasks")
    remote_storage_path = fields.CharField(max_length=255, unique=True)
    created_by = fields.ForeignKeyField("models.SysUser", related_name="tasks")
    creation_timestamp = fields.DatetimeField(auto_now_add=True)
