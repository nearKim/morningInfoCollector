import typing

from django.http import QueryDict
from rest_framework import views
from weather.requests import weather_api_requests
from weather.services import default_weather_service


class VillageWeatherAPIView(views.APIView):
    def get(self, request, format=None):
        query_params: QueryDict = request.query_params
        api_url = default_weather_service.get_full_weather_api_url(query_params)
        response = weather_api_requests.get(api_url)
        weather_api_items: typing.List[dict] = response.get("items")

        weather_history = default_weather_service.create_weather_forecast_history(
            weather_api_items
        )

        return response
