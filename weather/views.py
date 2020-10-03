from django.http import QueryDict
from django.utils import timezone
from rest_framework import views
from weather.services import default_weather_service


class VillageWeatherAPIView(views.APIView):
    def get(self, request, format=None):
        query_params: QueryDict = request.query_params
        x, y = query_params.get("x"), query_params.get("y")
        weather_api_items = default_weather_service.call_weather_api(query_params)
        weather_forecast_dto = default_weather_service.convert_response_to_dto(
            weather_api_items, timezone.now().date(), x=x, y=y
        )
        # TODO


class VillageWeatherInformationSendAPIView(views.APIView):
    def post(self, request, format=None):
        data = request.data
        x, y = data.get("x"), data.get("y")
        weather_api_items = default_weather_service.call_weather_api(data)
        weather_forecast_dto = default_weather_service.convert_response_to_dto(
            weather_api_items, timezone.now().date(), x=x, y=y
        )
        default_weather_service.create_simple_history(weather_forecast_dto)
        # TODO: 슬랙, 카카오톡, 이메일 등 처리
