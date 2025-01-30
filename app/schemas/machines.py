from pydantic import BaseModel, IPvAnyAddress, validator
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.machine import Machine

# Esquemas Pydantic
machine_pydantic = pydantic_model_creator(Machine, name="Machine")
machine_pydanticIn = pydantic_model_creator(Machine, name="MachineIn", exclude_readonly=True)

# Esquema para crear una maquina
class MachineCreate(BaseModel):
    name: str
    ip: IPvAnyAddress
    mac_address: str | None = None

    @validator("mac_address")
    def validate_mac_address(mac: str):
        """Valida la dirección MAC si está presente."""
        if mac and not len(mac) == 17:
            raise ValueError("MAC address must have exactly 17 characters")
        return mac
