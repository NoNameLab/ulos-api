from app.models.machine import Machine
from app.schemas.machines import MachineCreate, machine_pydantic

async def create_machine(machine: MachineCreate):
    """Crea una nueva máquina."""
    machine_obj = await Machine.create(**machine.model_dump(exclude_unset=True))
    return await machine_pydantic.from_tortoise_orm(machine_obj)

async def get_machine(machine_id: int):
    """Recupera una máquina por su ID."""
    machine = await Machine.get_or_none(id=machine_id)
    return await machine_pydantic.from_tortoise_orm(machine) if machine else None

async def update_machine(machine_id: int, machine: MachineCreate):
    """Actualiza una máquina existente."""
    machine_obj = await Machine.get_or_none(id=machine_id)
    if not machine_obj:
        return None
    await machine_obj.update_from_dict(machine.model_dump(exclude_unset=True)).save()
    return await machine_pydantic.from_tortoise_orm(machine_obj)

async def delete_machine(machine_id: int) -> bool:
    """Elimina una máquina por su ID."""
    deleted_count = await Machine.filter(id=machine_id).delete()
    return deleted_count > 0
