import datetime
import typing

from django.conf import settings
from django.utils import timezone
from django.utils.http import urlencode
from weather.dataclasses import (
    PrecipitationProbability,
    PrecipitationType,
    PtyCode,
    SkyStatus,
    SkyStatusCode,
    WeatherForecastDTO,
    WeatherRequestDTO,
)

__all__ = ["default_weather_service"]


DATE_FORMAT = "%Y%M%d"
API_ROOT = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"


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
    def get_full_weather_api_url(self, **query_params) -> str:
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

    def convert_response_to_dto(
        self,
        weather_api_responses: list,
        forecast_target_date: datetime.date,
        *,
        x: int,
        y: int,
    ):
        forecast_target_date_string = forecast_target_date.strftime("%Y%m%d")
        data = {
            "forecast_date": forecast_target_date,
            "x": x,
            "y": y,
            "probability_of_precipitation_list": [],
            "precipitation_type_list": [],
            "sky_status_list": [],
        }

        for weather_item in weather_api_responses:
            if weather_item.get("fcst_date") != forecast_target_date_string:
                continue
            category = weather_item.get("category")
            forecast_time = datetime.time(int(weather_item.get("fcst_time").strip("0")))
            value = weather_item.get("fcst_value")

            if category == "TMN":
                data["min_temperature"] = float(value)
            elif category == "TMX":
                data["max_temperature"] = float(value)
            elif category == "POP":
                value = PrecipitationProbability(forecast_time, value)
                data["probability_of_precipitation_list"].append(value)
            elif category == "PTY":
                value = PrecipitationType(forecast_time, PtyCode[value])
                data["precipitation_type_list"].append(value)
            elif category == "SKY":
                value = SkyStatus(forecast_time, SkyStatusCode[value])
                data["sky_status_list"].append(value)
        return WeatherForecastDTO(**data)


default_weather_service = WeatherService()
