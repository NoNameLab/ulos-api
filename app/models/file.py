from tortoise.models import Model
from tortoise import fields

class File(Model):
    id = fields.IntField(pk=True)
    task = fields.ForeignKeyField('models.Task', related_name='files', on_delete=fields.CASCADE)
    name = fields.CharField(max_length=255, null=True)
    path = fields.CharField(max_length=255, null=True)
    uploaded_at = fields.DatetimeField(auto_now_add=True)