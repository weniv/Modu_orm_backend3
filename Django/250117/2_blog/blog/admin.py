from django.contrib import admin
from .models import Post, Tag, Category, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]
    list_display_links = ["title"]
    list_filter = ["created_at"]
    search_fields = ["title"]


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
