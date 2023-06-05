import sqlite3
import datetime
from typing import Dict

__all__ = ['creating_data_base', 'insert_into_data_base', 'get_data_from_data_base']


def creating_data_base() -> None:
    """
    Функция создает БД если она не найдена
    """
    # Подключаемся к БД
    db = sqlite3.connect('server.db', isolation_level=None)
    cursor = db.cursor()  # Создаем объект курсора

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS `history`(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TINYTEXT,
    history_sms TINYTEXT,
    data_action DATETIME
    )""")

    db.close()  # Закрываем соединение с БД


def insert_into_data_base(info: Dict) -> None:
    """
    Функция записывает данные в БД

    :param info: Dict
        Получает словарь
    """
    # Подключаемся к БД
    db = sqlite3.connect('server.db', isolation_level=None)
    cursor = db.cursor()  # Создаем объект курсора
    # Создаем время когда пользователь воспользовался какой-то из команд
    info['data'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = (info)

    cursor.execute("""
    INSERT INTO `history`(name, history_sms, data_action)
    VALUES(:name, :history, :data)
    """, data)

    db.close()  # Закрываем соединение с БД


def get_data_from_data_base(name: str) -> str:
    """
    Функция запрашивает данные из БД по полному имени пользователя

    :param name: str
        Получаем полное имя пользователя

    :return: str
        Возвращаем в виде строки историю пользователя
    """
    # Подключаемся к БД
    db = sqlite3.connect('server.db')
    cursor = db.cursor()  # Создаем объект курсора

    data = ({'name': name})

    cursor.execute("""
    SELECT
        data_action,
        history_sms
    FROM history
    WHERE name = :name
    ORDER BY data_action DESC
    LIMIT 10
    """, data)

    info_string = ''
    response = cursor.fetchall()  # Получаем SELECT запрос

    count = 0
    for i_elem in response:
        count += 1
        info_string += f'{count}) {i_elem[0]}: {i_elem[1]}\n'

    db.close()  # Закрываем соединение с БД

    return info_string
