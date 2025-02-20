# from django import forms
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comment


class PostListSerializer(serializers.ModelSerializer):
    class AuthorSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["username"]

    # user = serializers.CharField(source="user.username")
    user = AuthorSerializer(read_only=True)

    status_label = serializers.CharField(source="get_status_display", read_only=True)

    @classmethod
    def get_optimized_queryset(cls):
        qs = Post.objects.filter(status=Post.Status.PUBLISHED)
        return qs.select_related("user")  # JOIN
        # return Post.objects.all().prefetch_related("user")  # NO JOIN

    class Meta:
        model = Post
        fields = [
            "pk",
            "user",
            "content",
            "photo",
            "status",
            "status_label",
            "created_at",
            "updated_at",
        ]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["pk", "content", "photo", "status", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["pk", "message", "created_at", "updated_at"]
