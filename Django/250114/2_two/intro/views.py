from django.shortcuts import render
from django.http import HttpResponse

"""
from .views import greeting, intro, announcement, esg
"""


def greeting(request):
    return HttpResponse("Hello, Django!")


def intro(request):
    return HttpResponse("Welcome to Django!")


def announcement(request):
    return HttpResponse("New announcement!")


def esg(request):
    return HttpResponse("ESG page")
