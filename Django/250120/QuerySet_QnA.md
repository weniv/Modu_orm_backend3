# QuerySet은 중복을 허용한다! Distinct()를 사용해야 한다!

```python
cd model_test
django-admin startproject config .
python manage.py startapp blog


# settings.py

INSTALLED_APPS = [
    "...",
    "blog",
]

####################################

python manage.py migrate
python manage.py createsuperuser

# hojun
# ghwns1234!

####################################
# blog/models.py

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

####################################
# blog/admin.py

from django.contrib import admin
from .models import Post

admin.site.register(Post)

####################################

python manage.py makemigrations
python manage.py migrate

# Q&A
# distinct()는 중복을 제거하는 함수입니다.
# 그런데 QuerySet은 중복이 없는 데이터를 가지고 있기 때문에
# distinct()를 사용해도 결과가 변하지 않습니다.
# 그래서 아래와 같은 간단한 예제(데이터의 중복이 없음을 확신할 때)
# 에서는 distinct()를 사용하지 않아도 됩니다.

# 그러면 언제 distinct()를 사용해야 할까요?
# 예를 들어, templates에서 중복된 게시물이 보일 때 사용을 고려해주시면 됩니다.

python manage.py shell
>>> from blog.models import Post
>>> from django.db.models import Q
>>> from django.contrib.auth.models import User
>>> user = User.objects.first()      
>>> Post.objects.create(title='title1', content='content11', author=user)
<Post: title1>
>>> Post.objects.create(title='title2', content='content22', author=user) 
<Post: title2>
>>> Post.objects.create(title='title3', content='content33', author=user) 
<Post: title3>
## 1이 들어간 title, content를 가진 QuerySet, filter
>>> a = Post.objects.filter(Q(title__contains='1'))
>>> a
<QuerySet [<Post: title1>]>
## 2와 3이 들어간 content를 가진 QuerySet, filter
>>> b = Post.objects.filter(Q(content__contains='1') | Q(content__contains='2') | Q(content__contains='3'))
>>> b
# a와 b를 합친 QuerySet, 다만 | 연산은 중복을 제거
>>> c = a | b
>>> c

# 아래 결과도 역시나 중복이 없기 때문에 distinct()를 사용하지 않아도 됩니다.
>>> Post.objects.create(title='hello', content='hello', author=user)
<Post: hello>
>>> result = Post.objects.filter(Q(title__contains='hello') | Q(content__contains='hello'))
>>> len(result)
1
>>> result
<QuerySet [<Post: hello>]>
>>> result = Post.objects.filter(Q(title__contains='hello') | Q(content__contains='hello')).distinct()
>>> len(result)
1
>>> result
<QuerySet [<Post: hello>]>

# 아래의 결과는 distinct()를 사용해야 합니다.
####################################
# blog/models.py

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

####################################
# blog/admin.py
from django.contrib import admin
from .models import Post, Tag

admin.site.register(Post)
admin.site.register(Tag)

####################################

python manage.py makemigrations
python manage.py migrate

python manage.py shell

>>> from blog.models import Post, Tag
>>> from django.contrib.auth.models import User
>>> user = User.objects.first()

# 태그 생성
>>> tag1 = Tag.objects.create(name='python')
>>> tag2 = Tag.objects.create(name='django')
>>> tag3 = Tag.objects.create(name='database')

# 게시물 생성 및 태그 추가
>>> post1 = Post.objects.create(title='Python 기초', content='파이썬 기초 내용', author=user)
>>> post1.tags.add(tag1, tag2)  # python, django 태그 추가

>>> post2 = Post.objects.create(title='Django로 웹 개발하기', content='장고 내용', author=user)
>>> post2.tags.add(tag2, tag3)  # django, database 태그 추가

# distinct()가 필요한 쿼리
# python 또는 django 태그가 있는 게시물 검색
>>> posts = Post.objects.filter(tags__name__in=['python', 'django'])
>>> len(posts)  # 결과: 3 (post1이 중복으로 카운트됨)
>>> posts
<QuerySet [<Post: Python 기초>, <Post: Python 기초>, <Post: Django로 웹 개발하기>]>
>>> posts = Post.objects.filter(tags__name__in=['python', 'django']).distinct()
>>> len(posts)  # 결과: 2 (중복 제거됨)
```