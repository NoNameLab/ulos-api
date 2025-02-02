from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from tortoise import Tortoise

ENV_PATH = ".env"

class Settings(BaseSettings):
    ENV: str = "development"
    APP_NAME: str = "ULOS-API"
    APP_VERSION: str = "1.0.0"

    DATABASE_TYPE: str = "postgres"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "sample"
    DATABASE_HOST: str = "localhost"
    DATABASE_NAME: str = "database"
    DATABASE_PORT: int = 5432

    ACCESS_TOKEN_SECRET_KEY: str = "sample"
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(case_sensitive=True, env_file=ENV_PATH)

env = None

try:
    env = Settings()

    TORTOISE_ORM = {
        "connections": {
            "default": {
                "engine": f"tortoise.backends.asyncpg",
                "credentials": {
                    "host": env.DATABASE_HOST,
                    "port": env.DATABASE_PORT,
                    "user": env.DATABASE_USER,
                    "password": env.DATABASE_PASSWORD,
                    "database": env.DATABASE_NAME,
                },
            }
        },
        "apps": {
            "models": {
                "models": ["app.models"],
                "default_connection": "default",
            },
        },
    }

    Tortoise.init_models(["app.models"], "models")
except ValidationError as e:
    print("A validation error has ocurred in config file {ENV_PATH}: {e}")