from tortoise import fields
from tortoise.models import Model

class TaskLog(Model):
    id = fields.BigIntField(pk=True)
    task = fields.ForeignKeyField("models.Task", related_name="logs")
    log_message = fields.TextField()
    creation_timestamp = fields.DatetimeField(auto_now_add=True)