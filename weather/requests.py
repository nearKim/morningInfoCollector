from json.decoder import JSONDecodeError

import requests
from rest_framework.exceptions import ParseError


class WeatherAPIRequest:
    def get(self, url, **kwargs):
        response = requests.get(url, **kwargs)
        try:
            res = response.json()
        except JSONDecodeError:
            raise ParseError('JSON 파싱에 실패했습니다. 요청 파라미터가 잘못되었을 수 있습니다.')

    def process_json(self, json):
        res = json.get('response
        header = res.get('header')









