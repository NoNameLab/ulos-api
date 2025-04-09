from tortoise import fields
from tortoise.models import Model

class TaskDefinition(Model):
    id = fields.IntField(pk=True)
    definition_name = fields.CharField(max_length=255, unique=True)
    definition_description = fields.TextField()
    creation_timestamp = fields.DatetimeField(auto_now_add=True)
