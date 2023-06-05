from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackDataFilter
from all_class.fsm_class import Custom
from all_class.factory_callback import choice_rated, choice_genre
from keyboard_for_bot import inline_kb_to_choice_genre, inline_kb_to_choice_next_page
from api_requests import get_start_info_custom, remove_photo
from all_class import show_more
from work_a_data_base import insert_into_data_base

__all__ = ['register_callback_query_handler_custom']


async def get_answer_rated(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Функция для записи выбранного рейтинга пользователя

    :param callback: CallbackQuery
        Callback

    :param state: FSMContext
        Машинное состояние
    """
    # Переход в машинное состояние: ожидание выбора жанра
    await Custom.genre.set()
    # Записываем полученный ответ о рейтинге в память
    rated_from_callback = callback.data.split(':')[2]

    match rated_from_callback:

        case ('top_rated_250' | 'top_rated_lowest_100') as rated:
            async with state.proxy() as data_storage:
                data_storage['rated'] = rated

        case 'no rated':
            async with state.proxy() as data_storage:
                data_storage['rated'] = None

    inline_keyboard = inline_kb_to_choice_genre()  # Получаем инлайн-клавиатуру

    await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
    await callback.bot.send_message(chat_id=callback.from_user.id,
                                    text='Хорошо, теперь выбери <b>жанр</b> по которому будем искать!',
                                    parse_mode='HTML',
                                    reply_markup=inline_keyboard)


async def get_answer_genre(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Функция для получения и записи о выбранном жанре пользователем

    :param callback: CallbackQuery
        Callback
    :param state: FSMContext
        Машинное состояние
    """
    # Переход в машинное состояние: ожидание выбора стартового диапозона года
    await Custom.start_year.set()
    # Записываем полученный ответ о жанре в память
    genre_from_callback = callback.data.split(':')[2]
    async with state.proxy() as data_storage:
        data_storage['genre'] = genre_from_callback

    await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
    await callback.bot.send_message(chat_id=callback.from_user.id,
                                    text='Хорошо, теперь введи <b>год</b> с которого мы будем искать в формате 0000, '
                                         'к сожалению мы сейчас обновляем базу, но фильмы все до 2020 года доступны '
                                         'для поиска',
                                    parse_mode='HTML')


async def show_next_page_user(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Функция описывает callback для показа следующей страницы или отмены просмотра

    photo_group: List
        Содержит список ссылок на интро-картины фильмов

    info_string: str
        Содержит строку с названиями и рейтингом фильмов

    data_from_state: Dict
        Получаем словарь данных из FSMState

    inline_keyboard_for_next_page: InlineKeyboardMarkup
        Получаем инлайн-клавиатуру для не/показа следующей страницы

    media_photo: MediaGroup
        Передаем в нее список интро-картин фильмов
    """
    data_from_callback = callback.data.split(':')[2]
    match data_from_callback:
        case 'show_me':
            # Отправляем данные для записи в БД
            data = {'name': callback.from_user.full_name,
                    'history': 'Просмотр след. страницы фильмов с определёнными  характеристиками'}
            insert_into_data_base(data)

            # Записываем данные в память FSMState
            async with state.proxy() as data_storage:
                data_storage['page'] += 1

            data_from_state = await state.get_data()
            # print(f'\nДанные из показа следующей страницы:\n\t{data_from_state}')

            info_string, photo_group = get_start_info_custom(data_from_state)
            inline_keyboard_for_next_page = inline_kb_to_choice_next_page()
            media_photo = types.MediaGroup(photo_group)

            # Проверяем если в info_string пришло None, уведомляем пользователя о том что ничего нет
            if info_string is None:
                await callback.bot.send_message(chat_id=callback.from_user.id,
                                                text='Прости, но нечего показать')
                await state.finish()  # Сбрасываем состояние

                return

            await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
            await types.ChatActions.upload_photo(sleep=3)  # Имитируем что мы загружаем фото

            # Отправляем информацию о фильмах пользователю
            await callback.bot.send_message(chat_id=callback.from_user.id,
                                            text=info_string)
            # Отправляем фотографии фильмов пользователю
            await callback.bot.send_media_group(chat_id=callback.from_user.id,
                                                media=media_photo)
            remove_photo()  # Удаляем фотографии после отправки

            await callback.bot.send_message(chat_id=callback.from_user.id,
                                            text='Еще показать?',
                                            reply_markup=inline_keyboard_for_next_page)

        case 'dont_show':
            await callback.answer(text='Ну нет так нет')  # Отвечаем
            await state.finish()  # Выходим из машинного состояния
            # print('\nЯ все отменил, вышел из машинного состояния')


def register_callback_query_handler_custom(dp: Dispatcher) -> None:
    """
    Регистрация callback для исполнения их в основном файле

    :param dp: Dispatcher
        Диспетчер
    """
    dp.register_callback_query_handler(get_answer_rated,
                                       CallbackDataFilter(factory=choice_rated, config={'type': 'info'}),
                                       state=Custom.rated)
    dp.register_callback_query_handler(get_answer_genre,
                                       CallbackDataFilter(factory=choice_genre, config={'type': 'info'}),
                                       state=Custom.genre)
    dp.register_callback_query_handler(show_next_page_user,
                                       CallbackDataFilter(factory=show_more, config={'type': 'info'}),
                                       state=Custom.page)
