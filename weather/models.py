from django.db import models


class WeatherForecastHistory(models.Model):
    WEATHER_CODE_TO_MODEL_FIELD_MAP = {
        "POP": "probability_of_precipitation",
        "PTY": "precipitation_type",
        "R06": "precipitation_six_hours",
        "REH": "humidity",
        "SKY": "sky_status",
        "T3H": "temperature_three_hours",
        "TMN": "min_temperature",
        "TMX": "max_temperature",
        "WSD": "wind_speed",
    }

    class SkyCode(models.IntegerChoices):
        맑음 = 1
        구름많음 = 3
        흐림 = 4

    class PtyCode(models.IntegerChoices):
        없음 = 0
        비 = 1
        진눈개비 = 2
        눈 = 3
        소나기 = 4
        빗방울 = 5
        빗방울_눈날림 = 6
        눈날림 = 7

    forecast_datetime = models.DateTimeField(verbose_name="예보일시")
    base_datetime = models.DateTimeField(verbose_name="발표일시", unique=True)

    probability_of_precipitation = models.IntegerField(verbose_name="강수확률")
    precipitation_type = models.IntegerField(choices=PtyCode, verbose_name="강수형태")
    precipitation_six_hours = models.IntegerField(verbose_name="6시간 강수량")
    humidity = models.IntegerField(verbose_name="습도")
    sky_status = models.IntegerField(choices=SkyCode, verbose_name="하늘 상태")
    temperature_three_hours = models.IntegerField(verbose_name="3시간 기온")
    min_temperature = models.IntegerField(verbose_name="최저기온")
    max_temperature = models.IntegerField(verbose_name="최고기온")
    wind_speed = models.IntegerField(verbose_name="풍속")

    # 참고: 기상청18_동네예보 조회서비스_오픈API활용가이드_격자_위경도(20200706)
    x = models.IntegerField(verbose_name="예보지점 X좌표")
    y = models.IntegerField(verbose_name="예보지점 Y좌표")
