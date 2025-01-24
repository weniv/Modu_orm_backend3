from datetime import timedelta
from django.shortcuts import render
from .forms import BookForm, LoanForm, ReservationForm
from accounts.decorators import librarian_required
from .models import Book, Loan, Reservation
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.


def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "books/book_detail.html", {"book": book})


@librarian_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)  # commit=False로 임시저장
            book.available_quantity = book.total_quantity
            book.save()
            messages.success(request, "도서가 등록되었습니다.")  # 성공 메시지
            return redirect("books:book-detail", pk=book.pk)  # 도서 상세 페이지로 이동
    else:
        form = BookForm()
    return render(request, "books/book_form.html", {"form": form})


@librarian_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, "도서가 수정되었습니다.")
            return redirect("books:book-detail", pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, "books/book_form.html", {"form": form, "title": "도서 수정"})


@librarian_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "도서가 삭제되었습니다.")
        return redirect("books:book-list")
    return render(request, "books/book_confirm_delete.html", {"book": book})


@login_required
def loan_list(request):

    if request.user.is_librarian():
        loans = Loan.objects.all().order_by("-loan_date")
    else:
        loans = Loan.objects.filter(user=request.user).order_by("-loan_date")

    return render(request, "books/loan_list.html", {"loans": loans})


@login_required
def loan_create(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == "POST":
        form = LoanForm(request.POST, user=request.user, book=book)
        if form.is_valid():
            loan = form.save(commit=False)  # 대출 정보 저장
            loan.book = book
            loan.user = request.user
            loan.due_date = timezone.now() + timedelta(days=14)  # 14일 대출
            loan.save()
            book.decrease_quantity()
            messages.success(
                request,
                f"{book.title} 도서가 대출되었습니다. 반납일은 {loan.due_date.date()}입니다.",
            )
            return redirect("books:loan-list")
    else:
        form = LoanForm(user=request.user, book=book)

    return render(request, "books/loan_form.html", {"form": form, "book": book})


@login_required
def loan_return(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)

    if request.user != loan.user and not request.user.is_librarian():
        messages.error(request, "권한이 없습니다.")
        return redirect("books:loan-list")

    if request.method == "POST":
        if loan.status == "ACTIVE":
            loan.status = "RETURNED"
            loan.returned_date = timezone.now()
            loan.save()

            loan.book.increase_quantity()

            waiting_reservation = (
                Reservation.objects.filter(book=loan.book, status="WAITING")
                .order_by("reserved_date")
                .first()
            )

            if waiting_reservation:
                waiting_reservation.status = "AVAILABLE"
                waiting_reservation.save()
                messages.success(
                    request,
                    "도서가 반납되었습니다. 예약자가 있어 예약자에게 우선권이 부여됩니다.",
                )
            else:
                messages.success(request, "도서가 반납되었습니다.")

        return redirect("books:loan-list")
    else:
        messages.error(request, "잘못된 접근입니다.")
        return redirect("books:loan-list")


@librarian_required
def overdue_list(request):
    loans = Loan.objects.filter(status="ACTIVE", due_date__lt=timezone.now()).order_by(
        "due_date"
    )
    return render(
        request, "books/loan_list.html", {"loans": loans, "show_overdue": True}
    )


@login_required
def reservation_list(request):
    if request.user.is_librarian():
        reservations = Reservation.objects.all().order_by("reserved_date")
    else:
        reservations = Reservation.objects.filter(
            user=request.user, status__in=["WAITING", "AVAILABLE"]
        ).order_by("reserved_date")
    return render(
        request, "books/reservation_list.html", {"reservations": reservations}
    )


@login_required
def reservation_create(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == "POST":
        form = ReservationForm(request.POST, user=request.user, book=book)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.book = book
            reservation.user = request.user
            reservation.expiry_date = timezone.now() + timedelta(days=3)
            reservation.save()
            messages.success(request, f"{book.title} 도서가 예약되었습니다.")
            return redirect("books:reservation-list")

    else:
        form = ReservationForm(user=request.user, book=book)

    return render(request, "books/reservation_form.html", {"form": form, "book": book})


@login_required
def reservation_cancel(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if request.user != reservation.user and not request.user.is_librarian():
        messages.error(request, "권한이 없습니다.")
        return redirect("books:reservation-list")

    if request.method == "POST":
        reservation.status = "CANCELLED"
        reservation.save()
        messages.success(request, "예약이 취소되었습니다.")
        return redirect("books:reservation-list")
    else:
        messages.error(request, "잘못된 접근입니다.")
        return redirect("books:reservation-list")
