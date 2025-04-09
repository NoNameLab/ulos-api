from tortoise.models import Model
from tortoise import fields

class ProcessingContainer(Model):
    id = fields.IntField(pk=True)
    container_name = fields.CharField(max_length=255, unique=True)
    container_description = fields.TextField()
    task_definition = fields.ForeignKeyField("models.TaskDefinition", related_name="containers")
    processing_stage = fields.OneToOneField("models.ProcessingStage", related_name="container")
    remote_storage_path = fields.CharField(max_length=255, unique=True)
    run_command = fields.TextField(null=True)
    creation_timestamp = fields.DatetimeField(auto_now_add=True)