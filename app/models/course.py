from tortoise import fields
from tortoise.models import Model

class Course(Model):
    id = fields.IntField(pk=True)
    course_name = fields.CharField(max_length=255, unique=True)
    creation_timestamp = fields.DatetimeField(auto_now_add=True)