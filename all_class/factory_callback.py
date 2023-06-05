from aiogram.utils.callback_data import CallbackData

__all__ = ['answer_on_genre', 'show_more', 'choice_genre', 'choice_rated']

answer_on_genre = CallbackData('answer_high', 'action')  # Класс для создания инлайн-клавиатуры с/без жанра
choice_genre = CallbackData('genre', 'type', 'choice')  # Класс для создания инлайн-клавиатуры с жанрами для user
show_more = CallbackData('show_more', 'type', 'action')  # Класс для инлайн-клавиатуры для не/вывода следующей страницы

choice_rated = CallbackData('rated', 'type', 'answer')  # Класс для выбора низкого/высокого рейтинга в /custom
