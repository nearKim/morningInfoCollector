from django.db import models


class SimpleForecastHistory(models.Model):
    forecast_date = models.DateField(auto_now_add=True)
    max_temperature = models.FloatField(verbose_name="최고기온")
    min_temperature = models.FloatField(verbose_name="최저기온")

    # 참고: 기상청18_동네예보 조회서비스_오픈API활용가이드_격자_위경도(20200706)
    x = models.IntegerField(verbose_name="예보지점 X좌표")
    y = models.IntegerField(verbose_name="예보지점 Y좌표")

    class Meta:
        unique_together = ["forecast_date", "x", "y"]
