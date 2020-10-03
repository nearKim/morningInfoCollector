from django.urls import include, path

from .views import VillageWeatherAPIView, VillageWeatherInformationSendAPIView

app_name = "weather"
urlpatterns = [
    path(
        "api/",
        include(
            [
                path(
                    "village",
                    VillageWeatherAPIView.as_view(),
                    name="village-weather-api",
                ),
                path(
                    "send",
                    VillageWeatherInformationSendAPIView.as_view(),
                    name="village-weather-information-send-api",
                ),
            ]
        ),
    )
]
