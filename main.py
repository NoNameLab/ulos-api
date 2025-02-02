from fastapi import FastAPI
from app.config.database import init_db

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
