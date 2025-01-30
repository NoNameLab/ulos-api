from fastapi import APIRouter, HTTPException
from app.services.machines import create_machine, get_machine, update_machine, delete_machine
from app.schemas.machines import MachineCreate, machine_pydantic

router = APIRouter(prefix="/machines", tags=["Machines"])

@router.post("/", response_model=machine_pydantic, status_code=201)
async def create_machine_endpoint(machine: MachineCreate):
    """Crea una nueva máquina."""
    return await create_machine(machine)

@router.get("/{machine_id}", response_model=machine_pydantic)
async def get_machine_endpoint(machine_id: int):
    """Recupera una máquina por su ID."""
    machine = await get_machine(machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine

@router.put("/{machine_id}", response_model=machine_pydantic)
async def update_machine_endpoint(machine_id: int, machine: MachineCreate):
    """Actualiza una máquina existente."""
    updated_machine = await update_machine(machine_id, machine)
    if not updated_machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return updated_machine

@router.delete("/{machine_id}", status_code=204)
async def delete_machine_endpoint(machine_id: int):
    """Elimina una máquina por su ID."""
    if not await delete_machine(machine_id):
        raise HTTPException(status_code=404, detail="Machine not found")
    return {"detail": "Machine deleted successfully"}
