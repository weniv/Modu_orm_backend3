from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    ROLE_CHOICES = [
        ('LIBRARIAN', '사서'),
        ('USER', '일반 사용자'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER',
        verbose_name='역할'
    )

    phone = models.CharField(max_length=20, blank=True,verbose_name='전화번호')

    class Meta: # Meta 클래스를 통해 모델의 메타데이터(옵션) 설정
       verbose_name = '사용자' # verbose_name 필드는 단수형 이름
       verbose_name_plural = '사용자 목록' # verbose_name_plural 필드는 복수형 이름