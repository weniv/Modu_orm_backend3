from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='도서명')
    author = models.CharField(max_length=50, verbose_name='저자')
    publisher = models.CharField(max_length=50, verbose_name='출판사')
    isbn = models.CharField(max_length=20, verbose_name='ISBN', unique=True)

    total_quantity = models.PositiveIntegerField(verbose_name='총 보유 수량')

    available_quantity = models.PositiveIntegerField(verbose_name='대출 가능 수량')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')

    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일시')

    class Meta:
        verbose_name = '도서'
        verbose_name_plural = '도서 목록'
        ordering = ['-created_at']  # 기본 정렬 순서

    def __str__(self):
        return self.title

    def is_available(self):
        return self.available_quantity > 0

    def decrease_quantity(self):
        if self.available_quantity > 0:
            self.available_quantity -= 1
            self.save()
            return True
        return False

    def increase_quantity(self):
        """반납 시 수량 증가"""
        if self.available_quantity < self.total_quantity:
            self.available_quantity += 1
            self.save()
            return True
        return False
