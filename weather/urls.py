from django.urls import include, path

from .views import VillageWeatherAPIView

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
            ]
        ),
    )
]
