from pydantic import BaseModel, EmailStr, validator
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.user import User
user_pydantic = pydantic_model_creator(User, name="User")
user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    role: str

    @validator("role")
    def validate_role(cls, value):
        if value not in {"student", "admin"}:
            raise ValueError("Role must be 'student' or 'admin'")
        return value

    @validator("email")
    def validate_email(cls, value):
        if not value.endswith("@uniandes.edu.co"):
            raise ValueError("Email must end with @uniandes.edu.co")
        return value