from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Tuple, Dict
from all_class import answer_on_genre, show_more, choice_genre, choice_rated

__all__ = ['keyboard_for_start_command', 'keyboard_for_help_command', 'inline_kb_to_answer_the_genre',
           'inline_kb_to_choice_genre', 'inline_kb_to_choice_next_page', 'genre',
           'inline_kb_to_choice_rated']
# ********************************  Клавиатура для файла main_commands_bot  *************************************


def keyboard_for_start_command() -> ReplyKeyboardMarkup:
    """
    Создаю клавиатуру для команды /start

    :return: ReplyKeyboardMarkup
        Возвращаю клавиатуру
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='/help'))

    return keyboard


def keyboard_for_help_command() -> Tuple[str, ReplyKeyboardMarkup]:
    """
    Создаю клавиатуру для команды /help и описание для нее

    :return: Tuple(str, ReplyKeyboardMarkup)
        возвращает описание команд, а так же клавиатуру
    """
    description = '/<b>start</b> - команда запускает бота\n' \
                  '/<b>high</b> - выводит топ фильмов с хорошим рейтингом\n' \
                  '/<b>low</b> - выводит топ фильмов с плохим рейтингом\n' \
                  '/<b>custom</b> - вывод фильмов по заданным параметрам\n' \
                  '/<b>cancel</b> - отмена, сброс\n' \
                  '/<b>help</b> - выводит список команд\n ' \
                  '/<b>history</b> - показать историю'

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(KeyboardButton(text='/high')).insert(KeyboardButton(text='/low'))
    keyboard.add(KeyboardButton(text='/custom')).insert(KeyboardButton(text='/help'))
    keyboard.add(KeyboardButton(text='/cancel')).insert(KeyboardButton(text='/history'))

    return description, keyboard


# ********************************  Клавиатура для общих комманд *************************************

def inline_kb_to_answer_the_genre() -> InlineKeyboardMarkup:
    """
    Создаю инлайн-клавиатуру для выбора пользователем с/без жанра

    :return: InlineKeyboardMarkup
        Возвращает инлайн клавиатуру
    """
    ikb = InlineKeyboardMarkup()
    ikb.add(InlineKeyboardButton(text='Выбрать жанр', callback_data=answer_on_genre.new('Genre')))
    ikb.add(InlineKeyboardButton(text='Без жанра', callback_data=answer_on_genre.new('No genre')))

    return ikb


genre: Dict = {
    "Action": 'Экшен',
    "Adult": 'Взрослые',
    "Adventure": 'Приключение',
    "Animation": 'Анимационные',
    "Biography": 'Биография',
    "Comedy": 'Комедия',
    "Crime": 'Криминал',
    "Documentary": 'Документальные',
    "Drama": 'Драма',
    "Family": 'Семейный',
    "Fantasy": 'Фантастика',
    "Film-Noir": 'Фильм-нуар',
    "Game-Show": 'Игровое-шоу',
    "History": 'История',
    "Horror": 'Ужасы',
    "Music": 'Музыкальный',
    "Musical": 'Мюзикл',
    "Mystery": 'Тайна',
    "Romance": 'Романтика',
    "Sci-Fi": 'Научной-фантастический',
    "Short": 'Короткий',
    "Sport": 'Спортивный',
    "Thriller": 'Триллер',
    "War": 'Военный',
    "Western": 'Вестерн'
}


# removed_genre = {
#     "News": 'Новости',
#     "Reality-TV": 'Реалити-шоу',
#     "Talk-Show": 'Ток-шоу',
# }

def inline_kb_to_choice_genre() -> InlineKeyboardMarkup:
    """
    Создаю инлайн-кавиатуру с жанрами для выбора жанра пользователем

    :return: InlineKeyboardMarkup
        Возвращаю инлайн клавиатуру
    """
    global genre

    ikb = InlineKeyboardMarkup()
    count = 1

    for i_en, i_ru in genre.items():
        if count % 2 == 0:
            ikb.insert(InlineKeyboardButton(text=i_ru, callback_data=choice_genre.new(type='info', choice=i_en)))
            count += 1
            continue

        ikb.add(InlineKeyboardButton(text=i_ru, callback_data=choice_genre.new(type='info', choice=i_en)))
        count += 1

    return ikb


def inline_kb_to_choice_next_page() -> InlineKeyboardMarkup:
    """
    Создаю инлайн-клавиатуру для вывода следующей страницы

    :return: InlineKeyboardMarkup
        Возвращаю инлайн-клавиатуру
    """
    ikb = InlineKeyboardMarkup()

    ikb.add(InlineKeyboardButton(text='Показать еще', callback_data=show_more.new(type='info',
                                                                                  action='show_me')))
    ikb.add(InlineKeyboardButton(text='Не надо', callback_data=show_more.new(type='info',
                                                                             action='dont_show')))

    return ikb


def inline_kb_to_choice_rated() -> InlineKeyboardMarkup:
    """
    Создаю инлайн-клавиатуру для выбора рейтинга пользователем

    :return: InlineKeyboardMarkup
        Возвращаю инлайн-клавиатуру
    """
    ikb = InlineKeyboardMarkup()

    ikb.add(InlineKeyboardButton(text='Высокий', callback_data=choice_rated.new(type='info',
                                                                                answer='top_rated_250')))
    ikb.add(InlineKeyboardButton(text='Низкий', callback_data=choice_rated.new(type='info',
                                                                               answer='top_rated_lowest_100')))
    ikb.add(InlineKeyboardButton(text='Просто ищи', callback_data=choice_rated.new(type='info',
                                                                                   answer='no rated')))

    return ikb
