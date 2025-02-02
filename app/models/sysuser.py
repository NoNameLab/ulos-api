from tortoise import fields
from tortoise.models import Model
from enum import Enum

class RoleEnum(str, Enum):
    ASSISTANT = 'assistant'
    PROFESSOR = 'professor'
    STUDENT = 'student'
    SYSADMIN = 'sysadmin'

class SysUser(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    assigned_role = fields.CharEnumField(RoleEnum)
    creation_timestamp = fields.DatetimeField(auto_now_add=True)