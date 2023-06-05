__all__ = ['handler_string']


def handler_string(data) -> str:
    """
    Функциия формирует строку с фильмами и рейтингом для вывода ее пользователю в Telegram

    :param data: List
        Внутри которого лежат Dict к каждому фильму с названием и рейтингом

    :return: str
        Возвращаем готовую строку для пользователя
    """
    info_string = ''
    count = 0

    for i_name in data:
        count += 1
        info_string += '{number}) Название: {name_movie} Рейтинг: {rating}\n'.format(
            number=count, name_movie=i_name['name'], rating=i_name['rating']
        )

    return info_string
