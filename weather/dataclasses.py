import datetime
import typing
from dataclasses import asdict, dataclass
from enum import Enum

from morningInfoCollector.utils import to_camel_case


class SkyStatusCode(Enum):
    맑음 = 1
    구름많음 = 3
    흐림 = 4


class PtyCode(Enum):
    없음 = 0
    비 = 1
    진눈개비 = 2
    눈 = 3
    소나기 = 4
    빗방울 = 5
    빗방울_눈날림 = 6
    눈날림 = 7


@dataclass
class WeatherRequestDTO:
    base_date: str = None
    base_time: str = None
    nx: int = None
    ny: int = None
    num_of_rows: typing.Optional[int] = None
    page_no: typing.Optional[int] = None
    data_type: typing.Union["JSON", "XML"] = "JSON"

    def serialize(self) -> dict:
        dictionary = asdict(self)
        date, time = dictionary.pop("base_date", None), dictionary.pop(
            "base_time", None
        )
        dictionary = {to_camel_case(k): v for k, v in dictionary.items() if v}

        if date and time:
            # base_date, base_time만 snake_case이다
            dictionary["base_date"] = date
            dictionary["base_time"] = time

        return dictionary


@dataclass
class PrecipitationProbability:
    forecast_time: datetime.time
    value: float


@dataclass
class PrecipitationType:
    forecast_time: datetime.time
    value: PtyCode


@dataclass
class SkyStatus:
    forecast_time: datetime.time
    value: SkyStatusCode


@dataclass
class WeatherForecastDTO:
    forecast_date: datetime.date
    x: int
    y: int
    probability_of_precipitation_list: typing.List[PrecipitationProbability]
    precipitation_type_list: typing.List[PrecipitationType]
    sky_status_list: typing.List[SkyStatus]
    min_temperature: typing.Optional[float] = None
    max_temperature: typing.Optional[float] = None

    def serialize(self) -> dict:
        dictionary = asdict(self)
        dictionary.pop("probability_of_precipitation_list")
        dictionary.pop("precipitation_type_list")
        dictionary.pop("sky_status_list")
        return dictionary
