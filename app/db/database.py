from tortoise import Tortoise, run_async

from app.core.settings import TORTOISE_ORM

async def init():
    await Tortoise.init(config=TORTOISE_ORM)

run_async(init())