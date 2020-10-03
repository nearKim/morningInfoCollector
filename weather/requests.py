from json.decoder import JSONDecodeError

import requests
from morningInfoCollector.utils import to_snake_dict
from requests import Response


class BaseError(Exception):
    def capture(self):
        # TODO
        pass


class ApplicationError(BaseError):
    pass


class DBError(BaseError):
    pass


class NoDataError(BaseError):
    pass


class APIHttpError(BaseError):
    pass


class TimeOutError(BaseError):
    pass

class InvalidRequestParameterError(BaseError):
    pass

class NoMandatoryParameterError(BaseError):
    pass


class ServiceKeyNotRegisteredError(BaseError):
    pass


class UnknownError(BaseError):
    pass


class WeatherAPIRequest:
    def get(self, url, **kwargs):
        response: Response = requests.get(url, **kwargs)

        if kwargs.get("raw", False):
            return response

        json = self.process_response(response)
        self.raise_error(json)

        return to_snake_dict(json["body"])

    def process_response(self, response: Response):
        response.raise_for_status()

        try:
            res_json = response.json().get("response")
        except JSONDecodeError:
            raise UnknownError("JSON 파싱에 실패했습니다. 요청 파라미터가 잘못되었을 수 있습니다.")
        return res_json

    def raise_error(self, json):
        header = json.get("header")
        if not header:
            raise UnknownError("기상청 API Response에 header키가 없습니다.")
        result_code = header.get("resultCode")

        if result_code == "00":
            # 정상
            return
        elif result_code == "01":
            raise ApplicationError
        elif result_code == "02":
            raise DBError
        elif result_code == "03":
            raise NoDataError
        elif result_code == "04":
            raise APIHttpError
        elif result_code == "05":
            raise TimeOutError
        elif result_code == "10":
            raise InvalidRequestParameterError
        elif result_code == "11":
            raise NoMandatoryParameterError
        elif result_code == "ServiceKeyNotRegisteredError":
            raise ServiceKeyNotRegisteredError
        else:
            raise UnknownError(f"에러코드: {result_code}")


weather_api_requests = WeatherAPIRequest()
