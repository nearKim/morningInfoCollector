import typing

from django.http import QueryDict
from django.utils import timezone
from rest_framework import views
from weather.requests import weather_api_requests
from weather.services import default_weather_service


class VillageWeatherAPIView(views.APIView):
    def _get(self, page_size=500, page_no=1, **query_params):
        api_url = default_weather_service.get_full_weather_api_url(
            page_size=page_size, page_no=page_no, **query_params
        )
        response = weather_api_requests.get(api_url)
        return response

    def get(self, request, format=None):
        query_params: QueryDict = request.query_params
        x, y = query_params.get("x", "y")
        response = self._get(**query_params)
        total_count = response.get("total_count")

        if total_count > 500:
            response = self._get(page_size=total_count, **query_params)

        weather_api_items: typing.List[dict] = response.get("items").get("item")

        weather_forecast_dto = default_weather_service.convert_response_to_dto(
            weather_api_items, timezone.now().date(), x=x, y=y
        )
        default_weather_service.create_simple_history(weather_forecast_dto)

        return response
