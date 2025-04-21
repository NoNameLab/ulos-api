# 1. Builder stage: instalar dependencias
FROM python:3.12-slim AS builder
WORKDIR /app

# Copiamos sólo requirements para cachear la instalación
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Runtime stage: copiamos código y deps
FROM python:3.12-slim
WORKDIR /app

# Traemos pip+paquetes instalados desde builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiamos el resto del código de tu proyecto
COPY . .

# Puerto en el que correrá FastAPI
EXPOSE 8000

# Arranca uvicorn apuntando a app/main.py (app: carpeta, main: módulo, app: instancia FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
