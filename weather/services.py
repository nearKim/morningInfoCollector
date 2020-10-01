import datetime
import typing

from django.conf import settings
from django.http import QueryDict
from django.utils import timezone
from django.utils.http import urlencode
from weather.dataclasses import WeatherRequestDTO
from weather.models import WeatherForecastHistory

__all__ = ["default_weather_service"]


DATE_FORMAT = "%Y%M%d"
API_ROOT = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"


def build_datetime(date_string: str, time_string: str):
    """ Weather API의 파라미터를 Python datetime 객체로 변환합니다 """
    clean_time = time_string.strip("00")
    result: datetime.datetime = datetime.datetime.strptime(
        f"{date_string} {clean_time}", "%Y%m%d %H"
    )
    return result


class WeatherAPIBuilder:
    def __init__(self):
        self.request_query = WeatherRequestDTO()

    def set_pagination(self, page_size, page_no):
        self.request_query.num_of_rows = page_size
        self.request_query.page_no = page_no
        return self

    def set_coordinates(self, x, y):
        self.request_query.nx = x
        self.request_query.ny = y
        return self

    def set_datetime(self, date: datetime.date, time: int = 5):
        if time not in [2, 5, 8, 11, 14, 17, 20, 23]:
            raise ValueError("시간대는 2, 5, 8, 11, 14, 17, 20, 23 중 하나여야 합니다.")

        if not date:
            date = timezone.now().date()
        self.request_query.date = date.strftime(DATE_FORMAT)
        self.request_query.time = f"0{time}00" if time < 10 else f"{time}00"
        return self

    def build(self) -> str:
        query_string = urlencode(self.request_query.serialize())
        service_key: str = settings.WEATHER_API_KEY
        return f"{API_ROOT}?serviceKey={service_key}&{query_string}"


class WeatherService:
    def get_full_weather_api_url(self, query_params: QueryDict) -> str:
        pagination: typing.Tuple[typing.Optional[int], typing.Optional[int]] = (
            query_params.get("page_size"),
            query_params.get("page_no"),
        )
        coordinates: typing.Tuple[int, int] = (
            query_params.get("x"),
            query_params.get("y"),
        )
        date = (
            datetime.datetime.strptime(query_params.get("date"), DATE_FORMAT).date()
            if "date" in query_params
            else None
        )
        date_and_time: typing.Tuple[
            typing.Optional[datetime.date], typing.Optional[int]
        ] = (date, query_params.get("time"))

        api_builder = WeatherAPIBuilder()
        api_url = (
            api_builder.set_datetime(*date_and_time)
            .set_coordinates(*coordinates)
            .set_pagination(*pagination)
            .build()
        )
        return api_url

    def create_weather_forecast_history(
        self, weather_api_responses: list
    ) -> WeatherForecastHistory:
        first_res = weather_api_responses[0]
        base_datetime = build_datetime(
            first_res.get("base_date"), first_res.get("base_time")
        )
        forecast_datetime = build_datetime(
            first_res.get("fcst_date"), first_res.get("fcst_time")
        )
        data = {
            "base_datetime": base_datetime,
            "forecast_datetime": forecast_datetime,
            "x": first_res.get("nx"),
            "y": first_res.get("ny"),
        }

        for response in weather_api_responses:
            weather_code = response.get("category")
            value = response.get("fcst_value")
            model_field_name = (
                WeatherForecastHistory.WEATHER_CODE_TO_MODEL_FIELD_MAP.get(weather_code)
            )
            data[model_field_name] = value

        return WeatherForecastHistory.objects.create(**data)


default_weather_service = WeatherService()
