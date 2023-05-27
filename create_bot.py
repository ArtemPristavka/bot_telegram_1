from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(token='')  # Сюда вставлять токен бота
dp = Dispatcher(bot=bot,
                storage=storage)
