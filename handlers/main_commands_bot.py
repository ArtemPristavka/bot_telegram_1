from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext, filters
from create_bot import bot  # dp - это что бы не забывать про диспетчер
from keyboard_for_bot import (keyboard_for_start_command, keyboard_for_help_command,
                              inline_kb_to_answer_the_genre, inline_kb_to_choice_rated)
from all_class.fsm_class import High, Low, Custom

__all__ = ['register_main_handlers']


async def start_command(message: types.Message) -> None:
    """
    Функция описывает команду /start для бота

    keyboard: ReplyKeyboardMarkup
        получет обычную клавиатуру для пользователя
    """
    keyboard = keyboard_for_start_command()

    await types.ChatActions.typing(sleep=2)  # Имитируем человека(показываем что бот что-то пишет)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Здраствуйте, я помогу вам найти фильмы для просмотра по разным критериям.'
                                '\nНажмите /<b>help</b> что бы увидеть список команд.',
                           parse_mode='HTML',
                           reply_markup=keyboard)


async def help_command(message: types.Message) -> None:
    """
    Функция описывает команду /help для бота

    description: str
        получает из функции описание доступных команд для пользователя

    keyboard: ReplyKeyboardMarkup
        получает обычную клавиатуру
    """
    description, keyboard = keyboard_for_help_command()

    await types.ChatActions.typing(sleep=2)  # Имитируем человека(показываем что бот что-то пишет)
    await bot.send_message(chat_id=message.from_user.id,
                           text=description,
                           parse_mode='HTML',
                           reply_markup=keyboard)


async def high_command(message: types.Message) -> None:
    """
    Функция описывает команду high для запроса пользователя

    inline_keyboard:  InlineKeyboardMarkup
        Получает инлайн клавиатуру
    """
    # Переход в машинное состояние: ожидание ответа от пользователя
    await High.answer.set()
    inline_keyboard = inline_kb_to_answer_the_genre()

    await types.ChatActions.typing(sleep=2)  # Имитируем человека(показываем что бот что-то пишет)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Хорошо. Просто вывести <b>топ фильмов</b> или выберишь <b>жанр</b>?\n',
                           parse_mode='HTML',
                           reply_markup=inline_keyboard)


async def low_command(message: types.Message) -> None:
    """
    Функция описывает команду /low для бота
    """
    # Переход в машинное состояние: ожидание ответа от пользователя
    await Low.answer.set()
    inline_keyboard = inline_kb_to_answer_the_genre()

    await types.ChatActions.typing(sleep=2)  # Имитируем человека(показываем что бот что-то пишет)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Хорошо. Просто вывести <b>топ фильмов</b> или выберишь <b>жанр</b>?\n',
                           parse_mode='HTML',
                           reply_markup=inline_keyboard)


async def custom_command(message: types.Message) -> None:
    # Переход в машинное состояние: ожидание ответа от пользователя о рейтинге
    await Custom.rated.set()
    inline_keyboard = inline_kb_to_choice_rated()

    await types.ChatActions.typing(sleep=2)  # Имитируем человека(показываем что бот что-то пишет)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Приступим. Выбери с каким <b>рейтингом</b> искать будем!',
                           parse_mode='HTML',
                           reply_markup=inline_keyboard)


async def cancel_command(message: types.Message, state: FSMContext) -> None:
    """
    Функция описывает команду /cancel для бота, для сброса машинного состония и выполнения команды

    get_fsm: State
        Получаем текущее FSM состояние у бота
    """
    get_fsm = await state.get_state()

    match get_fsm:
        case None:  # Если нет состояния
            # print('Сбрасывать нечего. Мы в обычном состоянии')
            pass

        case _:  # Если есть состояние
            await state.finish()
            # print('\nЯ все отменил, вышел из машинного состояния')

            await bot.send_message(chat_id=message.from_user.id,
                                   text='Я все отменил)))')


def register_main_handlers(dp: Dispatcher) -> None:
    """
    Регистрирую обработчики сообщений для использования в основном файле
    """
    dp.register_message_handler(callback=start_command, commands=filters.CommandStart().commands)
    dp.register_message_handler(callback=help_command, commands=filters.CommandHelp().commands)
    dp.register_message_handler(callback=high_command, commands=['high'])
    dp.register_message_handler(callback=low_command, commands=['low'])
    dp.register_message_handler(callback=custom_command, commands=['custom'])
    dp.register_message_handler(callback=cancel_command, commands=['cancel'], state='*')
