import abc
import datetime

import typing

from weather.dataclasses import WeatherForecastDTO, SkyStatusCode, PtyCode
from weather.models import SimpleForecastHistory


class AbstractTextCreator(abc.ABC):
    @abc.abstractmethod
    def create(self) -> typing.List[str]:
        """ 카카오톡 API 제한인 200자 미만인 str로 구성된 리스트를 반환합니다. """
        pass


class WeatherTextCreator(AbstractTextCreator):
    def __init__(self, dto: WeatherForecastDTO):
        yesterday = dto.forecast_date - datetime.timedelta(days=1)
        self.dto = dto
        self.yesterday_forecast_history: typing.Optional[
            SimpleForecastHistory
        ] = SimpleForecastHistory.objects.filter(
            forecast_date=yesterday, x=dto.x, y=dto.y
        ).first()

    def __get_relative_temperature_text(self, temperature: float):
        if temperature > 0:
            return f"어제보다 {temperature}℃ 높음"
        elif temperature < 0:
            return f"어제보다 {-temperature}℃ 낮음"
        else:
            return "어제와 동일함"

    def create_main_text(self):
        yesterday_min_temp_text = yesterday_max_temp_text = ""
        if self.yesterday_forecast_history:
            relative_min_temp = (
                self.yesterday_forecast_history.min_temperature
                - self.dto.min_temperature
            )
            relative_max_temp = (
                self.yesterday_forecast_history.max_temperature
                - self.dto.max_temperature
            )
            yesterday_min_temp_text = (
                f"({self.__get_relative_temperature_text(relative_min_temp)})"
            )
            yesterday_max_temp_text = (
                f"({self.__get_relative_temperature_text(relative_max_temp)})"
            )

        text = (
            f"[오늘의 날씨]\n"
            f"{self.dto.forecast_date.strftime('%m월 %d일')}\n"
            f"========"
            f"최소 기온: {self.dto.min_temperature}℃ {yesterday_min_temp_text}\n"
            f"최고 기온: {self.dto.max_temperature}℃ {yesterday_max_temp_text}"
        )
        return text

    def create_sky_status_text(self):
        text = "<하늘 상태>\n"
        time_text = sky_text = ""

        for sky in self.dto.sky_status_list:
            time = sky.forecast_time.strftime("%-H")
            time_text += f"{time}시\t"
            value = "값이 없습니다"
            if sky.value == SkyStatusCode.맑음:
                value = "(beam)"
            elif sky.value == SkyStatusCode.구름많음:
                value = "(confused)"
            elif sky.value == SkyStatusCode.흐림:
                value = "(worried)"

            sky_text += f"{value}\t"

        text += f"{time_text}\n"
        text += f"{sky_text}"
        return text

    def create_pop_text(self):
        text = "<강수 확률>\n"

        for pop in self.dto.probability_of_precipitation_list:
            time = pop.forecast_time.strftime("%-H")

            exclamation = ""
            if pop.value > 50:
                exclamation = "(sweat)"
            elif pop.value > 70:
                exclamation = "(sweat)" * 2

            text += f"{time}시: {pop.value} {exclamation}%\n"
        return text

    def create_pty_text(self):
        text = "<강수 유형>\n"

        time_text = pty_text = ""

        for pty in self.dto.precipitation_type_list:
            time = pty.forecast_time.strftime("%-H")
            time_text += f"{time}시\t"
            if pty.value in [PtyCode.비, PtyCode.소나기, PtyCode.빗방울]:
                value = "(rain)"
            elif pty.value == [PtyCode.진눈개비, PtyCode.눈, PtyCode.눈날림, PtyCode.빗방울_눈날림]:
                value = "(snow)"
            else:
                value = " - "
            pty_text += f"{value}\t"

        text += f"{time_text}\n"
        text += f"{pty_text}"
        return text

    def create(self) -> typing.List[str]:
        result = [
            self.create_main_text(),
            self.create_sky_status_text(),
            self.create_pop_text(),
            self.create_pty_text(),
        ]
        return [r.strip() for r in result]
