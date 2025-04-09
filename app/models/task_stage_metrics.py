from tortoise.models import Model
from tortoise import fields


class TaskStageMetrics(Model):
    id = fields.BigIntField(pk=True)
    task = fields.ForeignKeyField("models.Task", related_name="stage_metrics")
    processing_stage = fields.ForeignKeyField(
        "models.ProcessingStage", related_name="task_stage_metrics")
    time_interval = fields.TimeDeltaField(null=True)
    creation_timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together = ("task", "processing_stage")
