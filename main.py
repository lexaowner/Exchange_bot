import asyncio
import redis
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import TOKEN
from requests import *


redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(dp):
    try:
        redis_client.ping()
        print("Соединение с Redis установлено")
    except redis.exceptions.ConnectionError:
        print("Не удалось подключиться к Redis")


if __name__ == '__main__':
    from handlers import *
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)