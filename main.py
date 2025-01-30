from fastapi import FastAPI
from app.config.database import init_db
from app.routers.users import router as users_router
from app.routers.tasks import router as tasks_router
from app.routers.task_types import router as task_types_router
from app.routers.task_execution_logs import router as task_execution_logs_router
from app.routers.machines import router as machines_router
from app.routers.files import router as files_router
from app.routers.metrics import router as metrics_router

app = FastAPI(
    title="ULOS API",
    version="1.0.0",
    description="A FastAPI application to manage the ULOS database."
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the ULOS API!"}

# Inicializar la base de datos
init_db(app)

# Registrar routers
app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(task_types_router)
app.include_router(task_execution_logs_router)
app.include_router(machines_router)
app.include_router(files_router)
app.include_router(metrics_router)
