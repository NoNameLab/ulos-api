from tortoise import fields
from tortoise.models import Model

class Task(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    file_name = fields.CharField(max_length=255, null=True)
    ftp_file_path = fields.CharField(max_length=255, null=True)
    task_type_id = fields.IntField()
    parsed_status = fields.IntField(default=0)
    executed_status = fields.IntField(default=0)
    state = fields.IntField(default=0)
    requeue_count = fields.IntField(default=0)
    feedback = fields.TextField(null=True)