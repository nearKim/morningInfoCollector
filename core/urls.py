from core.views import kakao_auth_code_redirect_view
from django.urls import path

app_name = "core"
urlpatterns = [
    path(
        "kakao-auth-code-redirect/",
        kakao_auth_code_redirect_view,
        name="kakao-auth-code-redirect",
    )
]
