import json

import requests
from core.constants import KakaoTalk
from core.models import SimpleUser
from core.requests import kakao_api_requests
from django.conf import settings


class KakaoService:
    def create_token(self, email: str, code: str, redirect_uri: str) -> bool:
        user, _ = SimpleUser.objects.get_or_create(email=email)
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_APP_ID,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        response = requests.post(KakaoTalk.AUTH_TOKEN_API, data=data)

        if response.status_code == requests.codes.ok:
            r = response.json()
            user.kakao_user_token = r.get("access_token")
            user.kakao_refresh_token = r.get("refresh_token")
            user.save()
        else:
            # TODO: catch
            return False
        return True

    def refresh_token(self, user: SimpleUser) -> str:
        data = {
            "grant_type": "refresh_token",
            "client_id": settings.KAKAO_APP_ID,
            "refresh_token": user.kakao_refresh_token,
        }
        response = requests.post(KakaoTalk.AUTH_TOKEN_API, data=data)
        if response.status_code == requests.codes.ok:
            r = response.json()
            new_user_token = r.get("access_token")
            new_refresh_token = r.get("refresh_token")

            user.kakao_user_token = new_user_token
            if new_refresh_token:
                user.kakao_refresh_token = new_refresh_token

            user.save()
        else:
            # TODO: catch
            return ""
        # TODO: 사용자에게 refresh 되었다고 알려주기
        return new_user_token

    def send_message_to_me(
        self, user: SimpleUser, text, link=None, *, button_title: str = None
    ) -> bool:
        data = {"object_type": "text", "text": text, "link": link}

        if button_title:
            data["button_title"] = button_title
        result = kakao_api_requests.post(
            KakaoTalk.SEND_MESSAGE_TO_ME_API,
            user,
            data={"template_object": json.dumps(data)},
        )

        if not result.get("result_code") == 0:
            return False
        return True


default_kakao_service = KakaoService()
