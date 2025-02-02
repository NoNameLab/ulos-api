from tortoise import fields
from tortoise.models import Model

class StageByTaskDefinition(Model):
    id = fields.IntField(pk=True)
    task_definition = fields.ForeignKeyField("models.TaskDefinition", related_name="stages")
    processing_stage = fields.ForeignKeyField("models.ProcessingStage", related_name="task_definitions")

    class Meta:
        unique_together = ("task_definition", "processing_stage")