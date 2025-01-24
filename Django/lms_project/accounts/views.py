from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import LoginForm, UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# Create your views here.


def register_view(request):

    if request.user.is_authenticated:
        return redirect("accounts:profile")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "회원가입이 완료되었습니다.")  # 메시지 출력
            return redirect("accounts:profile")  # 프로필 페이지로 이동
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:  # 로그인 상태인 경우
        return redirect(reverse_lazy("accounts:profile"))  # 프로필 페이지로 이동
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "로그인 되었습니다.")
            return redirect(reverse_lazy("accounts:profile"))
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):

    if request.method == "POST":
        logout(request)
        messages.success(request, "로그아웃 되었습니다.")

    return redirect(reverse_lazy("accounts:login"))


@login_required
def profile_view(request):
    return render(
        request,
        "accounts/profile.html",
        {
            "active_loans": request.user.get_active_loans(),  # 현재 대출 중인 도서 목록
            "active_reservations": request.user.get_active_reservations(),  # 현재 예약 중인 도서 목록
        },
    )
