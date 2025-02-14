# blog/forms.py
#  - new/edit 뷰에서만 활용 (유효성 검사 및 저장)
#  - list/detail 뷰에서는 템플릿을 통해 HTML로 변환

from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
