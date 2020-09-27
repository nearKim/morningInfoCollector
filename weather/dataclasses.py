import typing
from dataclasses import dataclass, asdict
from morningInfoCollector.utils import to_camel_case


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
class WeatherResponseDTO:
    base_date: str
    base_time: str
    category: str
    fcst_date: str
    fcst_value: str
    nx: int
    ny: int
