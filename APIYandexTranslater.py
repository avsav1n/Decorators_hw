# https://netology.ru/profile/program/pyapi-104/lessons/375387/lesson_items/2034117
# https://yandex.ru/dev/dictionary/

import requests
from logger import Logger

@Logger.init
def translate_word(word):
    url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
    params = {
    'key': 'yandextoken',
    'lang': 'en-ru',
    'text': word
    }
    response = requests.get(url, params=params)
    trans_word = response.json()['def'][0]['tr'][0]['text']
    return trans_word

print(translate_word('dog'))
