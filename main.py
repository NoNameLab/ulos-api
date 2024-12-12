# C:\Uuu\FastAPIULOS\main.py
# uvicorn main:app --reload

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from routers.users_router import router as users_router
from routers.tasks_router import router as tasks_router
from routers.task_types_router import router as task_types_router
from routers.task_execution_logs_router import router as task_execution_logs_router
from routers.machines_router import router as machines_router
from routers.files_router import router as files_router
from routers.metrics_router import router as metrics_router



app = FastAPI(
    title="ULOS API",
    version="1.0.0",
    description="A FastAPI application to manage the ULOS database.",
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the ULOS API!"}

# Registrar los router 
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
app.include_router(task_types_router, prefix="/task_types", tags=["Task Types"])
app.include_router(task_execution_logs_router, prefix="/task_execution_logs", tags=["Task Execution Logs"])
app.include_router(machines_router, prefix="/machines", tags=["Machines"])
app.include_router(files_router, prefix="/files", tags=["Files"])
app.include_router(metrics_router, prefix="/metrics", tags=["Metrics"])


# Configuración de la conexión a ULOS en PostgreSQL
register_tortoise(
    app,
    db_url="postgres://postgres:123456789@localhost/ULOS",
    modules={"models": ["models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)
