from tortoise.models import Model
from tortoise import fields

class Machine(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    ip = fields.CharField(max_length=50, unique=True)
    mac_address = fields.CharField(max_length=17, unique=True, null=True)
