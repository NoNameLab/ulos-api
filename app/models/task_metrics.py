from tortoise.models import Model
from tortoise import fields

class TaskMetrics(Model):
    id = fields.BigIntField(pk=True)
    task = fields.ForeignKeyField("models.Task", related_name="metrics")
    requeue_count = fields.IntField(default=0)
    processing_time = fields.TimeDeltaField(null=True)
    parsing_time = fields.TimeDeltaField(null=True)
    execution_time = fields.TimeDeltaField(null=True)