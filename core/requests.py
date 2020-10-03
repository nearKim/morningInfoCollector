from functools import partial

import requests
from core.models import SimpleUser


class KakaoAPIRequest:
    def request(self, user: SimpleUser, method, url, *, headers=None, **kwargs):
        from core.services import default_kakao_service

        if not headers:
            headers = {"Authorization": f"Bearer {user.kakao_user_token}"}
        request = partial(
            requests.request, method=method, url=url, headers=headers, **kwargs
        )
        response = request()

        if response.status_code == 401:
            # Bearer Token이 유효하지 않을 경우
            kakao_user_token = default_kakao_service.refresh_token(user)
            headers = {"Authorization": f"Bearer {kakao_user_token}"}
            # TODO: response로 sentry catch
            return self.request(user, method, url, headers=headers, **kwargs)

        return self.process_response(response)

    def get(self, url, user, **kwargs):
        return self.request(user, "get", url=url, **kwargs)

    def post(self, url, user, **kwargs):
        return self.request(user, "post", url=url, **kwargs)

    def process_response(self, response):
        print(response)
        response.raise_for_status()
        body = response.json()

        return body


kakao_api_requests = KakaoAPIRequest()
