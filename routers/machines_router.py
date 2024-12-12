# C:\Uuu\FastAPIULOS\routers\machines_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, IPvAnyAddress
from tortoise.contrib.pydantic import pydantic_model_creator
from models import Machine

router = APIRouter()

# Esquemas Pydantic para Machine
Machine_Pydantic = pydantic_model_creator(Machine, name="Machine")
MachineIn_Pydantic = pydantic_model_creator(Machine, name="MachineIn", exclude_readonly=True)

class MachineCreate(BaseModel):
    machine_name: str
    machine_ip: IPvAnyAddress
    mac_address: str = None

    @staticmethod
    def validate_mac_address(mac: str):
        """
        Validar la dirección MAC si está presente.
        """
        if mac and not len(mac) == 17:
            raise ValueError("MAC address must have exactly 17 characters")
        return mac


@router.post("/", response_model=Machine_Pydantic, status_code=201)
async def create_machine(machine: MachineCreate):
    """
    Crea una nueva máquina en la base de datos.
    """
    machine_obj = await Machine.create(**machine.dict(exclude_unset=True))
    return await Machine_Pydantic.from_tortoise_orm(machine_obj)


@router.get("/{machine_id}", response_model=Machine_Pydantic)
async def get_machine(machine_id: int):
    """
    Recupera una máquina por su ID.
    """
    machine = await Machine.get_or_none(machine_id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return await Machine_Pydantic.from_tortoise_orm(machine)


@router.put("/{machine_id}", response_model=Machine_Pydantic)
async def update_machine(machine_id: int, machine: MachineCreate):
    """
    Actualiza una máquina existente.
    """
    machine_obj = await Machine.get_or_none(machine_id=machine_id)
    if not machine_obj:
        raise HTTPException(status_code=404, detail="Machine not found")
    await machine_obj.update_from_dict(machine.dict(exclude_unset=True)).save()
    return await Machine_Pydantic.from_tortoise_orm(machine_obj)


@router.delete("/{machine_id}", status_code=204)
async def delete_machine(machine_id: int):
    """
    Elimina una máquina por su ID.
    """
    deleted_count = await Machine.filter(machine_id=machine_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Machine not found")
    return {"detail": "Machine deleted successfully"}
