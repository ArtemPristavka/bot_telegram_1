import requests
import os
from PIL import Image
from aiogram import types
from typing import List

__all__ = ['download_photo', 'remove_photo']


def download_photo(data) -> List[types.InputMediaPhoto]:
    """
    Функция выполняет скачивания фотографий на сервер бота и
    отправку их на проверку по размерам в другую функию для Telegram

    :param data: List
        Получаем List внутри которого лежат Dict с фотографиями

    :return: List[types.InputMediaPhoto]
        Возвращает готовый список фотографий
    """
    photo_group = []

    count = 0
    for i_name in data:
        count += 1

        if i_name['image'] is not None:
            response_photo = requests.get(i_name['image'])
            get_path = os.getcwd()
            file_name = f'{get_path}/storage_photo/photo_{count}.jpg'
            # print(f'путь к файлу: {file_name}')

            with open(file=file_name, mode='wb') as save_photo:  # Скачиваем фотографию
                save_photo.write(response_photo.content)

            answer_from_photo = check_size_photo(file_name)  # Проверяем фото по размерам: если да то перезаписываем его
            if answer_from_photo is None:
                photo_group.append(types.InputMediaPhoto(types.InputFile(file_name)))
                continue
            else:
                answer_from_photo.save(file_name)
                photo_group.append(types.InputMediaPhoto(types.InputFile(file_name)))

    return photo_group


def check_size_photo(file_path) -> Image.Image | None:
    """
    Функция проверяет размеры фотографии по пикселям и если надо уменьшает их количество до нужного размера
    в равной пропорции что бы сохранялось соотношении сторон, а не обрезалось фотография

    :param file_path: str
        Путь к фотографии

    :return: Image.Image | None
        Возвращает отредактированную фотографию | None
    """
    work_photo = Image.open(file_path)  # Создаем объект этой фотографии что бы с ним работать
    width_photo = work_photo.size[0]  # Ширина фотографии
    height_photo = work_photo.size[1]  # Высота фотографии

    if (width_photo + height_photo) > 10 ** 4:
        all_summ_size = width_photo + height_photo  # Сумма всех пикселей
        need_to_norm = all_summ_size - 10 ** 4  # На сколько пикселей надо уменьшить

        width_percent = int((width_photo / all_summ_size * 100) + 1)  # Процент ширины от суммы всех пикселей
        height_percent = int((height_photo / all_summ_size * 100) + 1)  # Процент высоты от суммы всех пикселей

        will_width = int((need_to_norm * width_percent / 100) + 1)  # На сколько уменьшить ширину
        will_height = int((need_to_norm * height_percent / 100) + 1)  # На сколько уменьшить высоту

        new_width = width_photo - will_width  # Новая ширина фотографии
        new_height = height_photo - will_height  # Новая высота фотографии

        result = work_photo.resize((new_width, new_height))  # Изменяем размеры фотографии

        return result

    else:
        return None


def remove_photo() -> None:
    """
    Функция удаляет фотографии после отправки их пользователю, что бы бот не мусорил
    """
    get_current_path = os.getcwd()
    path_in_dir = f'{get_current_path}/storage_photo'

    for i_name in os.listdir(path_in_dir):
        if i_name.endswith('.jpg'):
            path_delete = os.path.join(path_in_dir, i_name)
            os.remove(path_delete)
            print(f'Удалили файл: {path_delete}')
