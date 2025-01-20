from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def accounts_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email", "")
        if not (username and password):
            return render(
                request,
                "accounts/accounts_signup.html",
                {"error": "아이디와 패스워드는 필수항목입니다."},
            )
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/accounts_signup.html",
                {"error": "가입하실 수 없는 아이디입니다."},
            )
        if User.objects.filter(email=email).exists():
            return render(
                request,
                "accounts/accounts_signup.html",
                {"error": "가입하실 수 없는 이메일입니다."},
            )
        # create_user와 create의 차이
        # create_user는 비밀번호를 암호화해서 저장
        # create는 비밀번호를 암호화하지 않고 저장
        # User(username, email)하고 나서
        # user.set_password(password)를 사용하면 비밀번호를 암호화해서 저장할 수 있음
        user = User.objects.create_user(username, email, password)
        user.save()
        auth_user = authenticate(username=username, password=password)
        # print(request.user.is_authenticated)
        login(request, auth_user)
        # print(request.user.is_authenticated)
        return redirect("accounts_profile")
    return render(request, "accounts/accounts_signup.html")


def accounts_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        auth_user = authenticate(username=username, password=password)
        if auth_user is not None:
            login(request, auth_user)
            return redirect("accounts_profile")
        return render(
            request,
            "accounts/accounts_login.html",
            {"error": "아이디 또는 비밀번호가 일치하지 않습니다."},
        )
    return render(request, "accounts/accounts_login.html")


def accounts_logout(request):
    # print(reqeust.user.is_authenticated)
    logout(request)
    # print(reqeust.user.is_authenticated)
    return redirect("accounts_login")


@login_required
def accounts_profile(request):
    return render(request, "accounts/accounts_profile.html")
