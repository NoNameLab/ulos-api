from tortoise import fields
from tortoise.models import Model

class ProcessingStage(Model):
    id = fields.IntField(pk=True)
    stage_name = fields.CharField(max_length=255, unique=True)
    stage_description = fields.TextField()