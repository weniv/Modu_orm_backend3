from django.shortcuts import render


def index(request):
    # print(request)
    # print(dir(request))
    context = {
        "name": "John",
        "age": 25,
        "is_true": True,
        "l": [1, 2, 3, 4, 5],
        "d": {"name": "John", "age": 25},
    }
    return render(request, "main/index.html", context)
