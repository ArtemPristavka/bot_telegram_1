from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboard_for_bot import inline_kb_to_choice_genre, inline_kb_to_choice_next_page
from api_requests import get_start_info_high, remove_photo
from aiogram.utils.callback_data import CallbackDataFilter
from all_class.fsm_class import High
from all_class.factory_callback import answer_on_genre, show_more, choice_genre
from work_a_data_base import insert_into_data_base

__all__ = ['register_callback_query_high']


async def callback_answer_genre(callback: types.CallbackQuery) -> None:
    """
    Функция описывает callback для выбора жанра пользователем

    inline_keyboard: InlineKeyboardMarkup
        Получает инлайн клавиатуру
    """
    # Переход в машинное состояние: ожидание выбора жанра
    await High.genre.set()

    inline_keyboard = inline_kb_to_choice_genre()
    # Имитируем человека бот что-то пишет
    await types.ChatActions.typing(sleep=2)

    await callback.bot.send_message(chat_id=callback.from_user.id,
                                    text='Хорошо. Выбери жанр, они ниже:',
                                    reply_markup=inline_keyboard)


async def callback_answer_no_genre(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Функция описывает callback если пользователь не стал выбирать жанр

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
    # Переход в машинное состояние: ожидание просмотра следующей страницы
    await High.page.set()
    # Записываем данные в память FSMState
    async with state.proxy() as data_storage:
        data_storage['genre'] = None
        data_storage['search'] = 'top_rated_250'
        data_storage['page'] = 1

    data_from_state = await state.get_data()
    # print(f'\nДанные из показа если не выбирали жанр: \n\t{data_from_state}')

    inline_keyboard_for_next_page = inline_kb_to_choice_next_page()
    info_string, photo_group = get_start_info_high(data_from_state)
    media_photo = types.MediaGroup(photo_group)

    # Проверяем если в info_string пришло None, уведомляем пользователя о том что ничего нет
    if info_string is None:
        await callback.bot.send_message(chat_id=callback.from_user.id,
                                        text='Прости, но нечего показать')
        await state.finish()  # Сбрасываем состояние

        return

    await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
    await types.ChatActions.upload_photo(sleep=2)  # Имитируем что мы загружаем фото

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

    # await callback.answer('Смотри!')


async def callback_broadcast_genre(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Функция описывает callback если пользователь выбрал жанр

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
    # Переход в машинное состояние: ожидание просмотра следующей страницы
    await High.page.set()
    # Записываем данные в память FSMState
    genre_from_callback = callback.data.split(':')[2]
    async with state.proxy() as data_storage:
        data_storage['genre'] = genre_from_callback
        data_storage['search'] = 'top_rated_250'
        data_storage['page'] = 1

    data_from_state = await state.get_data()
    # print(f'\nДанные из показа когда выбран жанр:\n\t{data_from_state}')

    inline_keyboard_for_next_page = inline_kb_to_choice_next_page()
    info_string, photo_group = get_start_info_high(data_from_state)
    media_photo = types.MediaGroup(photo_group)

    # Проверяем если в info_string пришло None, уведомляем пользователя о том что ничего нет
    if info_string is None:
        await callback.bot.send_message(chat_id=callback.from_user.id,
                                        text='Прости, но нечего показать')
        await state.finish()  # Сбрасываем состояние

        return

    await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
    await types.ChatActions.upload_photo(sleep=2)  # Имитируем что мы загружаем фото

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
                    'history': 'Просмотр след. страницы фильмов с высоким рейтингом'}
            insert_into_data_base(data)

            # Увеличиваем страницу для вывода информации пользователю
            async with state.proxy() as data_storage:
                data_storage['page'] += 1

            data_from_state = await state.get_data()
            # print(f'\nДанные из показа следующей страницы:\n\t{data_from_state}')

            info_string, photo_group = get_start_info_high(data_from_state)
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

            # await callback.answer(text='Смотри!')

        case 'dont_show':
            await callback.answer(text='Ну нет так нет')  # Отвечаем
            await state.finish()  # Выходим из машинного состояния
            print('\nЯ все отменил, вышел из машинного состояния')


def register_callback_query_high(dp: Dispatcher):
    """
    Регистрирую обработчики callback для исполнения их в основном файле
    """
    dp.register_callback_query_handler(callback_answer_genre,
                                       CallbackDataFilter(factory=answer_on_genre, config={'action': 'Genre'}),
                                       state=High.answer)

    dp.register_callback_query_handler(callback_answer_no_genre,
                                       CallbackDataFilter(factory=answer_on_genre, config={'action': 'No genre'}),
                                       state=High.answer)

    dp.register_callback_query_handler(callback_broadcast_genre,
                                       CallbackDataFilter(factory=choice_genre, config={'type': 'info'}),
                                       state=High.genre)

    dp.register_callback_query_handler(show_next_page_user,
                                       CallbackDataFilter(factory=show_more, config={'type': 'info'}),
                                       state=High.page)
