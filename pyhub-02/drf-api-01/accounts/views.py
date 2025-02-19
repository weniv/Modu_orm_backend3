from django.contrib.auth.views import LoginView, LogoutView


login = LoginView.as_view(
    # form_class=LoginForm,
    template_name="diary/form.html",
    # success_url_allowed_hosts=  # TODO:
)

# ?next= 지정을 추천
# settings.LOGOUT_REDIRECT_URL = "accounts:login"
# 이동 주소가 지정되지 않으면 로그아웃 후에, admin 페이지 스타일로 로그아웃 완료 메세지가 보여집니다.
logout = LogoutView.as_view(
    # success_url_allowed_hosts=  # TODO:
)
