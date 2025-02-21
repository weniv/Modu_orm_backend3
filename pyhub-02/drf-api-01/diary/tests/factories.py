# diary/tests/factories.py
#  - 반드시 diary/tests/__init__.py 빈 파일을 생성해줘야만 팩키지로 인식

import factory
from accounts.tests.factories import UserFactory
from diary.models import Post, Comment


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    content = factory.Faker("paragraphs", nb=3)
    status = "published"


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    message = factory.Faker("paragraph")
