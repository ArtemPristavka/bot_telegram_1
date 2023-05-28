from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(token='6105356535:AAH6-srqCo7uT60W8l2kGSkhzoFLSWOxTLI')  # Сюда вставлять токен бота
dp = Dispatcher(bot=bot,
                storage=storage)
