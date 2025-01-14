from django.shortcuts import render
from django.http import HttpResponse

"""
from .views import pressrelease, prgallary, archives
"""


def pressrelease(request):
    return HttpResponse("pressrelease")


def prgallary(request):
    return HttpResponse("prgallary")


def archives(request):
    return HttpResponse("archives")
