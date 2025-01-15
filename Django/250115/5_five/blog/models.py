from django.db import models


class Post(models.Model):
    # 글의 제목 (최대 100자)
    title = models.CharField(max_length=100)
    # 글의 내용
    content = models.TextField()
    # 글 작성 시간 (처음 생성 때 현재 시간 저장)
    created_at = models.DateTimeField(auto_now_add=True)
    # 글 수정 시간 (수정할 때마다 자동으로 갱신)
    updated_at = models.DateTimeField(auto_now=True)
    main_image = models.ImageField(upload_to="blog/", blank=True, null=True)

    def __str__(self):
        return f"{self.title}"
