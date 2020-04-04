import requests
from typing import Optional

API_TOKEN = 'trnsl.1.1.20200404T161735Z.78f7aa8a3c431e25.e5f7e051418f60fcaf420f672ef7cf47d147b19f'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
CODES = {
    401: 'Неправильный API-ключ',
    402: 'API-ключ заблокирован',
    404: 'Превышено суточное ограничение на объем переведенного текста',
    413: 'Превышен максимально допустимый размер текста',
    422: 'Текст не может быть переведен',
    501: 'Заданное направление перевода не поддерживается'
}

def translate(text: str):
    params = {
        'key': API_TOKEN,
        'text': text,
        'lang': 'ru'
    }
    try:
        response = requests.get(url=URL, params=params, timeout=5)
    except requests.exceptions.Timeout:
        return {
            'error': 'Таймоут'
        }
    if response.status_code == 200:
        return {
            'in': text,
            'out': response.json()['text'][0]
        }
    else:
        return {
            'error': CODES.get(response.status_code) or 'Что-то пошло не так'
        }

    