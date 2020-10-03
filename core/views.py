from core.services import default_kakao_service
from django.http import HttpResponse
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.request import Request


@api_view(["GET"])
def kakao_auth_code_redirect_view(request: Request):
    """ 카카오톡 로그인 완료 후 리다이렉트 uri를 통해 접근하게 되는 뷰 """
    if request.query_params.get("error") == "access_denied":
        return HttpResponse("취소되었습니다.")

    email = request.query_params.get("state")
    code = request.query_params.get("code")
    redirect_uri = request.build_absolute_uri(reverse("core:kakao-auth-code-redirect"))
    success = default_kakao_service.create_token(email, code, redirect_uri)
    if success:
        # TODO: 등록완료 이메일 보내기
        pass
    return HttpResponse("등록 완료")
