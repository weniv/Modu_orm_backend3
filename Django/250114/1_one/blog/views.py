from django.http import HttpResponse
from data import blog


def blog_list(request):
    result = ""
    for b in blog:
        result += f"{b['title']}<br>"
    return HttpResponse(result)


def blog_details(request, blog_id):
    return HttpResponse(f"blog details {blog[blog_id]}")
