from enum import Enum

from django.db import models

# TODO: Enum 다른 곳으로 리팩터
class SkyCode(Enum):
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


class WeatherForecastHistory(models.Model):
    class WeatherCode(models.TextChoices):
        POP = "POP", "강수확률"
        PTY = "PTY", "강수형태"
        R06 = "R06", "6시간 강수량"
        REH = "REH", "습도"
        SKY = "SKY", "하늘상태"
        T3H = "T3H", "3시간 기온"
        TMN = "TMN", "아침 최저기온"
        TMX = "TMX", "낮 최고기온"
        UUU = "UUU", "풍속(동서)"
        VVV = "VVV", "풍속(남북)"
        WAV = "WAV", "파고"
        VEC = "VEC", "풍향"
        WSD = "WSD", "풍속"

    forecast_datetime = models.DateTimeField(verbose_name="예보일시")
    base_datetime = models.DateTimeField(verbose_name="발표일시", unique=True)
    weather_code = models.CharField(
        choices=WeatherCode.choices, verbose_name="자료구분문자", max_length=3
    )
    forecast_value = models.CharField(max_length=30, verbose_name='예보 값')

    # 참고: 기상청18_동네예보 조회서비스_오픈API활용가이드_격자_위경도(20200706)
    x = models.IntegerField(verbose_name="예보지점 X좌표")
    y = models.IntegerField(verbose_name="예보지점 Y좌표")
