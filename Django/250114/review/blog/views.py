from django.shortcuts import render

blog_data = [
    {"id": 0, "title": "First Blog", "content": "This is my first blog."},
    {"id": 1, "title": "Second Blog", "content": "This is my second blog."},
]


def blog_list(request):
    context = {"blogs": blog_data}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    context = {"blog": blog_data[pk]}
    return render(request, "blog/blog_detail.html", context)
