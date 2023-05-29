from aiogram import executor
from create_bot import dp
import handlers
import os

handlers.register_callback_query_high(dp=dp)
handlers.register_callback_query_low(dp=dp)
handlers.register_main_handlers(dp=dp)
handlers.register_callback_query_handler_custom(dp=dp)
handlers.register_message_handler_custom(dp=dp)


if __name__ == '__main__':
    if not os.path.exists('storage_photo'):
        os.mkdir('storage_photo')
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
