# from django import forms
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["pk", "message", "created_at", "updated_at"]
