from django.views import View
from django.http import HttpResponse


class MyView(View):
    def get(self, request):
        return HttpResponse("Hello, World! GET!")

    def post(self, request):
        return HttpResponse("Hello, World! POST!")
