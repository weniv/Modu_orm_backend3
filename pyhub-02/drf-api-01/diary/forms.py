from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # 허용목록을 직접 작성하시어, 노출할 생각이 없었는 데, 모델에 추가된 필드가
        # 유저에게 자동 노출되는 것을 막으시는 것을 추천.
        fields = ["content", "photo", "status"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 유저로부터 입력받을 필드만 기입
        fields = ["message"]
