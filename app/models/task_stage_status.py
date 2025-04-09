from tortoise import fields
from tortoise.models import Model

class TaskStageStatus(Model):
    id = fields.IntField(pk=True)
    task = fields.ForeignKeyField("models.Task", related_name="stage_statuses")
    processing_stage = fields.ForeignKeyField("models.ProcessingStage", related_name="task_stage_statuses")
    processing_status = fields.ForeignKeyField("models.ProcessingStatus", related_name="task_stage_statuses")
    creation_timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together = ("task", "processing_stage")