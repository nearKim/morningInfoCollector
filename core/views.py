import requests
from core.models import SimpleUser
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.request import Request


@api_view(["GET"])
def kakao_auth_code_redirect_view(request: Request):
    """ 카카오톡 로그인 완료 후 리다이렉트 uri를 통해 접근하게 되는 뷰 """
    code = request.query_params.get("code")
    email = request.query_params.get("state")
    user, _ = SimpleUser.objects.get_or_create(email=email)
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.KAKAO_APP_ID,
        "redirect_uri": request.build_absolute_uri(
            reverse("core:kakao-auth-code-redirect")
        ),
        "code": code,
    }
    response = requests.post("https://kauth.kakao.com/oauth/token", data=data)

    if response.status_code == requests.codes.ok:
        r = response.json()
        user.kakao_user_token = r.get("access_token")
        user.kakao_refresh_token = r.get("refresh_token")
        user.save()
    else:
        # TODO: catch
        pass
    # TODO: 등록완료 이메일 보내기
    return HttpResponse("등록 완료")
