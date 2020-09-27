from json.decoder import JSONDecodeError

import requests
from django.http import QueryDict
from rest_framework import views
from weather.services import default_weather_service


class VillageWeatherAPIView(views.APIView):
    def get(self, request, format=None):
        query_params: QueryDict = request.query_params
        api_url = default_weather_service.get_full_weather_api_url(query_params)

        try:
            response = requests.get(api_url).json()
        except JSONDecodeError:
            raise APIError


        return response
