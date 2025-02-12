from django.db import models


# 관계형 데이터베이스 : MySQL, MariaDB, Oracle, PostgreSQL, SQLite, SQL Server
# NoSQL : MongoDB, etc.
# 요즘의 RDB => json 타입 지원

# 2개 이상의 DB 지원 : Router 지원

# str, int, float


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 카테고리
class Category(TimestampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # default 정렬

# 댓글
class Comment(TimestampedModel):
    post = models.ForeignKey(to="Post", on_delete=models.CASCADE)
    message = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']  # default 정렬

# 포스팅
class Post(TimestampedModel):
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    tag_set = models.ManyToManyField("Tag", blank=True)  # 다수의 태그 목록

    class Meta:
        ordering = ['-id']  # default 정렬


# 태그 : django-taggit
class Tag(TimestampedModel):
    name = models.CharField(max_length=100)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']  # default 정렬

# 팔로잉/팔로워
