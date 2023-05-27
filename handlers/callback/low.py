from create_bot import bot  # dp
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboard_for_bot import inline_kb_to_choice_genre, inline_kb_to_choice_next_page
from keyboard_for_bot import genre
from api_requests import get_start_info_high, remove_photo
from aiogram.utils.callback_data import CallbackDataFilter
from all_class.fsm_class import Low
from all_class.factory_callback import answer_on_genre, show_more

__all__ = ['register_callback_query_low']


async def callback_answer_genre(callback: types.CallbackQuery) -> None:
    """
    Функция описывает callback для выбора жанра пользователем

    inline_keyboard: InlineKeyboardMarkup
        Получает инлайн клавиатуру
    """
    # Переход в машинное состояние: ожидание выбора жанра
    await Low.genre.set()

    inline_keyboard = inline_kb_to_choice_genre()

    await types.ChatActions.typing(sleep=2)

    await bot.send_message(chat_id=callback.from_user.id,
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
    await Low.page.set()
    # Записываем данные в память FSMState
    async with state.proxy() as data_storage:
        data_storage['genre'] = None
        data_storage['search'] = 'top_rated_lowest_100'
        data_storage['page'] = 1

    data_from_state = await state.get_data()
    print(f'\nДанные из показа если не выбирали жанр: \n\t{data_from_state}')

    inline_keyboard_for_next_page = inline_kb_to_choice_next_page()
    info_string, photo_group = get_start_info_high(data_from_state)

    await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
    await types.ChatActions.upload_photo(sleep=2)  # Имитируем что мы загружаем фото
    media_photo = types.MediaGroup(photo_group)

    await bot.send_message(chat_id=callback.from_user.id,
                           text=info_string)

    await bot.send_media_group(chat_id=callback.from_user.id,
                               media=media_photo)
    remove_photo()  # Удаляем фотографии после отправки

    await bot.send_message(chat_id=callback.from_user.id,
                           text='Еще показать?',
                           reply_markup=inline_keyboard_for_next_page)
    await callback.answer('Смотри!')


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
    await Low.page.set()
    # Записываем данные в память FSMState
    async with state.proxy() as data_storage:
        data_storage['genre'] = callback.data
        data_storage['search'] = 'top_rated_lowest_100'
        data_storage['page'] = 1

    data_from_state = await state.get_data()
    print(f'\nДанные из показа когда выбран жанр:\n\t{data_from_state}')

    inline_keyboard_for_next_page = inline_kb_to_choice_next_page()
    info_string, photo_group = get_start_info_high(data_from_state)

    await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
    await types.ChatActions.upload_photo(sleep=2)  # Имитируем что мы загружаем фото
    media_photo = types.MediaGroup(photo_group)

    await bot.send_message(chat_id=callback.from_user.id,
                           text=info_string)

    await bot.send_media_group(chat_id=callback.from_user.id,
                               media=media_photo)
    remove_photo()  # Удаляем фотографии после отправки

    await bot.send_message(chat_id=callback.from_user.id,
                           text='Еще показать?',
                           reply_markup=inline_keyboard_for_next_page)
    await callback.answer(text='Смотри!')


async def show_next_page_user(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Функция описывает callback для показа следующей страницы

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
    # Записываем данные в память FSMState
    async with state.proxy() as data_storage:
        data_storage['page'] += 1

    data_from_state = await state.get_data()
    print(f'\nДанные из показа следующей страницы:\n\t{data_from_state}')

    info_string, photo_group = get_start_info_high(data_from_state)
    inline_keyboard_for_next_page = inline_kb_to_choice_next_page()

    await types.ChatActions.typing(sleep=2)  # Имитируем что мы что-то пишем
    await types.ChatActions.upload_photo(sleep=3)  # Имитируем что мы загружаем фото
    media_photo = types.MediaGroup(photo_group)

    await bot.send_message(chat_id=callback.from_user.id,
                           text=info_string)

    await bot.send_media_group(chat_id=callback.from_user.id,
                               media=media_photo)
    remove_photo()  # Удаляем фотографии после отправки

    await bot.send_message(chat_id=callback.from_user.id,
                           text='Еще показать?',
                           reply_markup=inline_keyboard_for_next_page)
    await callback.answer(text='Смотри!')


async def dont_show_page(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Функция описывает callback если пользователю не надо показывать следующую страницу
    """
    await callback.answer(text='Ну нет так нет')  # Отвечаем
    await state.finish()  # Выходим из машинного состояния
    print('\nЯ все отменил, вышел из машинного состояния')


def register_callback_query_low(dp: Dispatcher):
    """
    Регистрирую обработчики callback для исполнения их в основном файле
    """
    dp.register_callback_query_handler(callback_answer_genre,
                                       CallbackDataFilter(factory=answer_on_genre, config={'action': 'Genre'}),
                                       state=Low.answer)

    dp.register_callback_query_handler(callback_answer_no_genre,
                                       CallbackDataFilter(factory=answer_on_genre, config={'action': 'No genre'}),
                                       state=Low.answer)

    dp.register_callback_query_handler(callback_broadcast_genre,
                                       lambda callback: callback.data in genre.keys(),
                                       state=Low.genre)

    dp.register_callback_query_handler(show_next_page_user,
                                       CallbackDataFilter(factory=show_more, config={'action': 'show_me'}),
                                       state=Low.page)
    dp.register_callback_query_handler(dont_show_page,
                                       CallbackDataFilter(factory=show_more, config={'action': 'dont show'}),
                                       state=Low.page)
