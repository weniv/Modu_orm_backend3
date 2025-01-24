from django.utils import timezone
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

    def is_librarian(self):
        return self.role == 'LIBRARIAN'
    
    def can_borrow(self):
        from books.models import Loan
        active_loan = Loan.objects.filter(
            user=self,
            status="ACTIVE"
        ).count()
        return active_loan < 3

    def has_overdue_books(self):
        from books.models import Loan
        return Loan.objects.filter(
            user=self,
            status='ACTIVE',
            due_date__lt=timezone.now()
        ).exists()
    
    def get_active_loans(self):
        return self.loan_set.filter(status='ACTIVE')
    
    def get_active_reservations(self):
        return self.reservation_set.filter(status='ACTIVE')