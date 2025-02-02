from pydantic import BaseModel, EmailStr, validator
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.sysuser import SysUser, RoleEnum

sysuser_pydantic = pydantic_model_creator(SysUser, name="SysUser")
sysuser_pydanticIn = pydantic_model_creator(SysUser, name="SysUserIn", exclude_readonly=True)

class SysUserCreate(BaseModel):
    email: EmailStr
    password: str
    assigned_role: RoleEnum

    @validator("email")
    def validate_email(cls, v):
        if not v.endswith("@uniandes.edu.co"):
            raise ValueError("Email must be from uniandes domain")
        return v

class SysUserLogin(BaseModel):
    email: EmailStr
    password: str