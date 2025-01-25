from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="도서명")
    author = models.CharField(max_length=50, verbose_name="저자")
    publisher = models.CharField(max_length=50, verbose_name="출판사")
    isbn = models.CharField(max_length=20, verbose_name="ISBN", unique=True)

    total_quantity = models.PositiveIntegerField(verbose_name="총 보유 수량")

    available_quantity = models.PositiveIntegerField(verbose_name="대출 가능 수량")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일시")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        verbose_name = "도서"
        verbose_name_plural = "도서 목록"
        ordering = ["-created_at"]  # 기본 정렬 순서

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


class Loan(models.Model):

    STATUS_CHOICES = [
        ("ACTIVE", "대출 중"),
        ("OVERDUE", "연체"),
        ("RETURNED", "반납완료"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ACTIVE",
        verbose_name="대출 상태",
    )

    loan_date = models.DateTimeField(auto_now_add=True, verbose_name="대출일")

    due_date = models.DateTimeField(verbose_name="반납예정일")

    returned_date = models.DateField(blank=True, null=True, verbose_name="반납일")

    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="대출 도서")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="사용자"
    )

    class Meta:
        verbose_name = "대출"
        verbose_name_plural = "대출 목록"
        ordering = ["-loan_date"]  # 최신 대출 순으로 정렬

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def is_overdue(self):

        # 대출중이고 반납예정일이 지났으면 True 반환
        return self.status == "ACTIVE" and timezone.now() > self.due_date


class Reservation(models.Model):

    STATUS_CHOICES = [
        ("WAITING", "대기중"),
        ("AVAILABLE", "대출가능"),
        ("CANCELLED", "취소됨"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="WAITING",
        verbose_name="예약 상태",
    )

    reserved_date = models.DateTimeField(auto_now_add=True, verbose_name="예약일")

    expiry_date = models.DateTimeField(verbose_name="예약만료일")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="사용자"
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="예약 도서")

    class Meta:
        verbose_name = "예약"
        verbose_name_plural = "예약 목록"
        ordering = ["reserved_date"]  # 예약일 순으로 정렬
        # 한 사용자가 같은 도서를 중복 예약할 수 없도록 제약
        # 사용자, 도서, 상태가 같은 경우 중복 예약 방지
        unique_together = ["user", "book"]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def is_expired(self):
        return timezone.now() > self.expiry_date  # 예약 만료일이 지났으면 True 반환
