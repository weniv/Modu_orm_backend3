from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # \venv\Lib\site-packages\django\contrib\auth\models.py
    # 문자열로 참조하는 이유는 순환 참조를 피하기 위함
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
