from django.shortcuts import render
from django.http import HttpResponse


def accounts_details(request, username):
    return HttpResponse(f"accounts details {username}")
