from tortoise import fields
from tortoise.models import Model

class SysUser(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    creation_timestamp = fields.DatetimeField(auto_now_add=True)