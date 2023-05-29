from typing import Dict, Tuple, List
from .requests_for_high_and_low import handler_response
from .handler_info_text import handler_string
from .check_photo import download_photo
from aiogram import types
import requests
import json


__all__ = ['get_start_info_custom']


def get_start_info_custom(user_data: Dict) -> Tuple[str, List[types.InputMediaPhoto]] | Tuple[None, None]:
    url = "https://moviesdatabase.p.rapidapi.com/titles"
    querystring = dict()

    match user_data:
        case {'rated': 'top_rated_250', 'genre': str(genre), 'start_year': str(start_year),
              'end_year': str(end_year), 'page': int(page)}:
            querystring = {"genre": genre,
                           "startYear": start_year,
                           "list": "top_rated_250",
                           "page": str(page),
                           "info": "base_info",
                           "endYear": end_year}

        case {'rated': 'top_rated_lowest_100', 'genre': str(genre), 'start_year': str(start_year),
              'end_year': str(end_year), 'page': int(page)}:
            querystring = {"genre": genre,
                           "startYear": start_year,
                           "list": "top_rated_lowest_100",
                           "page": str(page),
                           "info": "base_info",
                           "endYear": end_year}

        case {'rated': None, 'genre': str(genre), 'start_year': str(start_year),
              'end_year': str(end_year), 'page': int(page)}:
            querystring = {"genre": genre,
                           "startYear": start_year,
                           "page": str(page),
                           "info": "base_info",
                           "endYear": end_year}

    headers = {"X-RapidAPI-Key": "643e7fe797msh701c941bef910b1p16f450jsnf37a447d1799",
               "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"}

    response = requests.get(url,
                            headers=headers,
                            params=querystring)

    data = json.loads(response.text)
    # Проверяем, если внутри ничего нет, то возвращем None
    if data['entries'] == 0:
        return None, None

    all_info = handler_response(data)
    info_string = handler_string(all_info)
    photos = download_photo(all_info)

    return info_string, photos
