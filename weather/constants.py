# 동네예보
from enum import Enum

API_ROOT = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"


class WeatherCode(Enum):
    POP = "강수확률"
    PTY = "강수형태"
    R06 = "6시간 강수량"
    REH = "습도"
    SKY = "하늘상태"
    T3H = "3시간 기온"
    TMN = "아침 최저기온"
    TMX = "낮 최고기온"
    UUU = "풍속(동서)"
    VVV = "풍속(남북)"
    WAV = "파고"
    VEC = "풍향"
    WSD = "풍속"

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
