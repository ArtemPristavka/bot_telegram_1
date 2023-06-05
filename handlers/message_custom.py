from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from all_class import Custom
from api_requests import get_start_info_custom, remove_photo
from keyboard_for_bot import inline_kb_to_choice_next_page
import re

__all__ = ['register_message_handler_custom']


async def get_start_year(message: types.Message, state: FSMContext) -> None:
    """
    Функция для проверки валидности и записи начального года поиска

    :param message: Message
        Обьект сообщения от пользователя
    :param state: FSMContext
        Машинное состояние
    """
    data = message.text
    check_year = re.compile(r'\d{4}')

    match data:
        # Проверяем строку на нужное нам значение, первый фильм вышел в 1895 году и год не должен быть меньше,
        # если он меньше то отвечаем ему
        case str() as year if re.match(check_year, year) and int(year) < 1895:
            await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
            await message.bot.send_message(chat_id=message.from_user.id,
                                           text='Помни: первый фильм вышел в 1895 году. '
                                                'Введи заново:')

        # Проверям строку на нужный год, он не должен быть выше 2020 года, так как выше это значения фильмов нету,
        # если так то отвечаем ему
        case str() as year if re.match(check_year, year) and int(year) > 2020:
            await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
            await message.bot.send_message(chat_id=message.from_user.id,
                                           text='Я же говорил, что мы сейчас обновляем базу данных, '
                                                'максимально возможный год 2020 ! Введи заново:')

        # Проверяем ввел ли пользователь год цифрами, если нет то отвечаем ему
        case str() as year if not re.match(check_year, year):
            await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
            await message.bot.send_message(chat_id=message.from_user.id,
                                           text='Это не цифры, пожалуйста введе цифрами:')

        # Проверяем то что год больше 1895, т.к выше обработчики он прошел, и записываем данные
        case str() as year if re.match(check_year, year) and int(year) >= 1895:
            # Переходим в следующие состояние: ожидание ввода конечного года диапозона
            await Custom.end_year.set()
            # Записываем полученные данные о начальном годе от пользователя
            async with state.proxy() as data_storage:
                data_storage['start_year'] = year

            await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
            await message.bot.send_message(chat_id=message.from_user.id,
                                           text='Хорошо, теперь введи год окончания поиска:')


async def get_end_year(message: types.Message, state: FSMContext) -> None:
    """
    Функция для проверки валидности и отправки данных в функцию для запроса к API

    :param message: Message
        Обьект сообщения от пользователя
    :param state: FSMContext
        Машинное состояние
    """
    data = message.text
    check_year = re.compile(r'\d{4}')
    data_from_state = await state.get_data()  # Берем данные из состояния
    start_year = data_from_state['start_year']  # Беред начальный год что бы сравниват его с тем что вводит пользователь

    match data:
        # Проверяем что бы го не был больше 2020 года, если больше то отвечаем
        case str() as year if re.match(check_year, year) and int(year) > 2020:
            await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
            await message.bot.send_message(chat_id=message.from_user.id,
                                           text='Помни то что мы обновляем базу, максимум 2020 год. '
                                                'Введи заново:')
            return

        # Проверяем что бы год окончания поиска не был меньше стартового года пользователя который он ввел,
        # если он ввел меньше то отвечаем ему
        case str() as year if re.match(check_year, year) and int(year) < int(start_year):
            await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
            await message.bot.send_message(chat_id=message.from_user.id,
                                           text='Погоди, вспомни какой стартовый год ты вводил!!! '
                                                'Введи заново, конечный год:')
            return

        # Проверяем ввел ли пользователь год цифрами, если нет то отвечаем ему
        case str() as year if not re.match(check_year, year):
            await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
            await message.bot.send_message(chat_id=message.from_user.id,
                                           text='Это не цифры, пожалуйста введе цифрами:')
            return

        # Если все предыдущие обработчики пройдены, то значение правильное и мы его записываем
        case str() as year:
            # Переходим в следующее состояние: ожидание просмотра след. страницы
            await Custom.page.set()
            # Записываем полученные данные о окончательном годе диапозона от пользователя
            async with state.proxy() as data_storage:
                data_storage['end_year'] = year
                data_storage['page'] = 1

    # Берем данные для передачи их в запрос
    data_for_request = await state.get_data()
    inline_keyboard_for_next_page = inline_kb_to_choice_next_page()
    info_string, photo_group = get_start_info_custom(data_for_request)
    media_photo = types.MediaGroup(photo_group)

    # Проверяем если в info_string пришло None, уведомляем пользователя о том что ничего нет
    if info_string is None:
        await message.bot.send_message(chat_id=message.from_user.id,
                                       text='Прости, но нечего показать')
        await state.finish()  # Сбрасываем состояние

        return

    await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
    await types.ChatActions.upload_photo(sleep=2)  # Имитируем что мы загружаем фото
    # Отправляем информацию о фильмах пользователю
    await message.bot.send_message(chat_id=message.from_user.id,
                                   text=info_string)
    # Отправляем фотографии фильмов пользователю
    await message.bot.send_media_group(chat_id=message.from_user.id,
                                       media=media_photo)
    remove_photo()  # Удаляем фотографии после отправки

    await message.bot.send_message(chat_id=message.from_user.id,
                                   text='Еще показать?',
                                   reply_markup=inline_keyboard_for_next_page)


def register_message_handler_custom(dp: Dispatcher) -> None:
    """
    Регистрирую обработчики для исполнения их в основном файле

    :param dp: Dispatcher
        Диспетчер
    """
    dp.register_message_handler(callback=get_start_year,
                                content_types=types.ContentTypes.TEXT,
                                state=Custom.start_year)

    dp.register_message_handler(callback=get_end_year,
                                content_types=types.ContentTypes.TEXT,
                                state=Custom.end_year)
