from tortoise import fields
from tortoise.models import Model

class ProcessingStatus(Model):
    id = fields.IntField(pk=True)
    status_name = fields.CharField(max_length=255, unique=True)
    status_description = fields.TextField()