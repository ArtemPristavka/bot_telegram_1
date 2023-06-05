from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import handlers
import os
from dotenv import load_dotenv
from aiogram.utils.exceptions import ValidationError
from work_a_data_base import creating_data_base


def register_handlers(dp) -> None:
    handlers.register_callback_query_high(dp)
    handlers.register_callback_query_low(dp)
    handlers.register_main_handlers(dp)
    handlers.register_callback_query_handler_custom(dp)
    handlers.register_message_handler_custom(dp)


def main():
    load_dotenv(dotenv_path='.env')
    BOT_TOKEN = os.getenv('TOKEN')

    if BOT_TOKEN == '' or BOT_TOKEN is None:
        raise ValidationError("Пожалуйста вставьте токен бота в '.env_template'")

    storage = MemoryStorage()
    bot = Bot(token=BOT_TOKEN)  # Сюда вставлять токен бота
    dp = Dispatcher(bot=bot,
                    storage=storage)

    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=register_handlers(dp))


if __name__ == '__main__':
    if not os.path.exists('storage_photo'):
        os.mkdir('storage_photo')
    creating_data_base()
    main()
