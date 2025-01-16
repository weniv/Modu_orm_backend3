from django.db import models


class Date(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:  # 이것은 이 모델이 데이터베이스 테이블을 생성하지 않고 다른 모델에게 필드를 상속해주기만 하는 추상 클래스임을 나타냅니다.
        abstract = True


class Post(Date):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return self.name


class Comment(Date):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    def __str__(self):
        return self.content
