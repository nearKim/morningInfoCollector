import typing
from django.core.management import BaseCommand
from core.creator import WeatherTextCreator, StockTextCreator
from core.models import SimpleUser
from core.services import default_kakao_service
from weather.services import default_weather_service

me, _ = SimpleUser.objects.get_or_create(email="cheshire0814@gmail.com")


class Command(BaseCommand):
    def handle_weather(self):
        dto = default_weather_service.get_weather_forecast_dto()
        default_weather_service.create_simple_history(dto)

        text_creator = WeatherTextCreator(dto)
        weather_text_list: typing.List[str] = text_creator.create()

        for text in weather_text_list:
            default_kakao_service.send_message_to_me(me, text)

    def handle_stock(self):
        text_creator = StockTextCreator()
        stock_text_list: typing.List[str] = text_creator.create()

        for text in stock_text_list:
            default_kakao_service.send_message_to_me(me, text)

    def handle(self, *args, **options):
        self.handle_weather()
        self.handle_stock()
