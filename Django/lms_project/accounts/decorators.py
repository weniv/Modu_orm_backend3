from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def librarian_required(view_func):

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "로그인이 필요한 서비스입니다.")
            return redirect("accounts:login")

        if not request.user.is_librarian():
            messages.error(request, "사서 권한이 필요합니다.")
            return redirect("accounts:profile")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
