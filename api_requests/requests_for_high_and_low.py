from typing import Dict, Tuple, List, Any
from aiogram import types
from .handler_info_text import handler_string
from .check_photo import download_photo
import json
import requests

__all__ = ['get_start_info_high']


def get_start_info_high(user_data: Dict) -> Tuple[str, List[types.InputMediaPhoto]]:
    """
    Функциия выполняет запрос к API и при помощи других функций формирует ответ

    :param user_data: Dict
        Получаем критерии запроса от пользователя

    :return: Tuple[str, List[types.InputMediaPhoto]]
        Возвращаем строку с описание всех фильмов и фотографии фильмов
    """
    url = "https://moviesdatabase.p.rapidapi.com/titles"
    querystring = dict()

    match user_data:
        case {'search': 'top_rated_250', 'page': int(page), 'genre': None, **kwargs} if not kwargs:
            querystring = {"list": "top_rated_250",
                           "page": str(page),
                           "info": "base_info",
                           "endYear": "2020"}

        case {'search': 'top_rated_250', 'page': int(page), 'genre': str(genre), **kwargs} if not kwargs:
            querystring = {"genre": genre,
                           "list": "top_rated_250",
                           "page": str(page),
                           "info": "base_info",
                           "endYear": "2020"}

        case {'search': 'top_rated_lowest_100', 'page': int(page), 'genre': None, **kwargs} if not kwargs:
            querystring = {"list": "top_rated_lowest_100",
                           "page": str(page),
                           "info": "base_info",
                           "endYear": "2020"}

        case {'search': 'top_rated_lowest_100', 'page': int(page), 'genre': str(genre), **kwargs} if not kwargs:
            querystring = {"genre": genre,
                           "list": "top_rated_lowest_100",
                           "page": str(page),
                           "info": "base_info",
                           "endYear": "2020"}

    headers = {"X-RapidAPI-Key": "643e7fe797msh701c941bef910b1p16f450jsnf37a447d1799",
               "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"}

    response = requests.get(url,
                            headers=headers,
                            params=querystring)

    data = json.loads(response.text)
    all_info = handler_response(data)
    info_string = handler_string(all_info)
    photos = download_photo(all_info)

    return info_string, photos


def handler_response(info: Dict) -> List[Dict[str, Any | None]]:
    """
    Функция вытаскивает всю нужную информацию из полученного ответа от API

    :param info: Dict
        Получаем Dict от API в котором вся информация лежит

    :return: List[Dict[str, Any | None]]
        Возвращает List внутри которого находятся Dict для каждого фильма
    """

    data = []

    for i_count in info['results']:

        photo_movie = i_count.get('primaryImage')
        if photo_movie is not None:
            photo_movie = photo_movie.get('url')

        rating_movie = i_count.get('ratingsSummary')
        if rating_movie is not None:
            rating_movie = rating_movie.get('aggregateRating')

        name_movie = i_count.get('titleText')
        if name_movie is not None:
            name_movie = name_movie.get('text')

        info_of_film = {'name': name_movie,
                        'rating': rating_movie,
                        'image': photo_movie}

        data.append(info_of_film)

    return data
