from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    role = fields.CharField(max_length=50, choices=["student", "admin"])
    created_at = fields.DatetimeField(auto_now_add=True)