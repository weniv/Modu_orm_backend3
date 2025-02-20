from django.db import models
from django.contrib.auth.models import User

# from accounts.models import User


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "초안"
        PUBLISHED = "published", "Published"
        DELETED = "deleted", "Deleted"

    user = models.ForeignKey(
        to=User,  # 현재 앱을 재사용하지 않는다면, 직접 User 모델 지정 OK.
        # to="auth.User",
        # 재사용하는 장고 앱을 만든다면, 프로젝트의 User가 바뀔 수 있어요.
        # to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diary_post_set",
        related_query_name="diary_post",
    )
    content = models.TextField()
    photo = models.ImageField(blank=True)  # Pillow 라이브러리 설치가 필요
    status = models.CharField(
        choices=Status.choices,  # 선택지를 제한 !!!
        # default="draft",
        default=Status.DRAFT,
        max_length=20,
    )

    # is_published = models.BooleanField()  # 2가지 값을 가지는 상태

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def soft_delete(self):
        self.content = ""
        self.status = self.Status.DELETED
        self.save()


class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="diary_comment_set",
        related_query_name="diary_comment",
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    # post = models.ForeignKey(Post, default=1, on_delete=models.SET_DEFAULT)

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
