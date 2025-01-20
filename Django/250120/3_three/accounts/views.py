from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import SignUpForm, LoginForm


def accounts_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accounts_profile")
    else:
        form = SignUpForm()
    return render(request, "accounts/accounts_signup.html", {"form": form})


def accounts_login(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("accounts_profile")
            # username = form.cleaned_data["username"]
            # password = form.cleaned_data["password"]
            # user = authenticate(request, username=username, password=password)
            # if user is not None:
            #     login(request, user)
            #     return redirect("accounts_profile")
    else:
        form = LoginForm()
    return render(request, "accounts/accounts_login.html", {"form": form})


def accounts_logout(request):
    # print(request.user.is_authenticated)
    logout(request)
    # print(request.user.is_authenticated)
    return redirect("accounts_login")


@login_required
def accounts_profile(request):
    return render(request, "accounts/accounts_profile.html")
