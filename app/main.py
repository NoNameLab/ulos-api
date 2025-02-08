from fastapi import FastAPI
from tortoise import exceptions as db_exception
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import TORTOISE_ORM, env
from app.routers import auth, courses, task_definitions, tasks

app = FastAPI(title=env.APP_NAME, version=env.APP_VERSION)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
try:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        add_exception_handlers=True
    )
except db_exception.ConfigurationError as e:
    print(f"An error has ocurred while configuring the database: {e}")
    raise e
except db_exception.DBConnectionError as e:
    print(f"An error has ocurred while connecting to the database: {e}")
    raise e

@app.get("/ok", tags=["health"])
async def health_check():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(courses.router)
app.include_router(task_definitions.router)
app.include_router(tasks.router)