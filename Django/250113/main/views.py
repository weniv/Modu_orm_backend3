from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Hello, world.</h1>")


def a(request):
    return HttpResponse("Hello, world a!")


def b(request):
    return HttpResponse("Hello, world b!")


def c(request):
    data1 = [10, 20, 30, 40]
    data2 = ["apple", "banana", "cherry", "date"]
    context = {"data1": data1, "data2": data2}
    return render(request, "main/c.html", context)
