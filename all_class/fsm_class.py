from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = ['High', 'Low']


class High(StatesGroup):
    """
    Класс описывающий FSM для команды /high и ее callback
    """
    answer = State()  # Ожидание ответа от пользователя: с/без жанра
    genre = State()  # Ожидание выбора жанра
    page = State()  # Ожидание просмотра следующей страницы


class Low(StatesGroup):
    """
    Класс описывающий FSM для команды /low и ее callback
    """
    answer = State()  # Ожидание ответа от пользователя: с/без жанра
    genre = State()  # Ожидание выбора жанра
    page = State()  # Ожидание просмотра следующей страницы
