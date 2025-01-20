from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path("signup/", views.accounts_signup, name="accounts_signup"),
    path("login/", views.accounts_login, name="accounts_login"),
    path("logout/", views.accounts_logout, name="accounts_logout"),
    path("profile/", views.accounts_profile, name="accounts_profile"),
    path("testurl/", lambda request: HttpResponse("testurl"), name="testurl"),
]
