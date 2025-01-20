from django.contrib import admin
from .models import Post

# class PostAdmin(admin.ModelAdmin):
#     list_display = ["title", "author"]

# admin.site.register(Post, PostAdmin)

admin.site.register(Post)
