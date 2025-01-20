from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.shortcuts import render

# \venv\Lib\site-packages\django\contrib\auth\views.py
accounts_signup = CreateView.as_view(
    form_class=UserCreationForm,
    template_name="accounts/accounts_signup.html",
    success_url=settings.LOGIN_URL,
)

accounts_login = LoginView.as_view(
    template_name="accounts/accounts_login.html",
    # next_page="/accounts/testurl/",
)

accounts_logout = LogoutView.as_view(
    next_page=settings.LOGIN_URL,
)


@login_required
def accounts_profile(request):
    return render(request, "accounts/accounts_profile.html")
