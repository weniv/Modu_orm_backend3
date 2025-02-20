from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "status", "created_at", "updated_at"]
    list_filter = ["status"]


# admin.site.register(Post, PostAdmin)

# Model: ModelAdmin = 1 : 1


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
