from django.shortcuts import render
from django.http import HttpResponse

"""
from .views import (
    notice,
    notice_detail,
    recruitment,
    recruitment_detail,
    other,
    other_detail,
)
"""


def notice(request):
    return HttpResponse("notice")


def notice_detail(request, pk):
    return HttpResponse(f"notice_detail {pk}")


def recruitment(request):
    return HttpResponse("recruitment")


def recruitment_detail(request, pk):
    return HttpResponse(f"recruitment_detail {pk}")


def other(request):
    return HttpResponse("other")


def other_detail(request, pk):
    return HttpResponse(f"other_detail {pk}")
