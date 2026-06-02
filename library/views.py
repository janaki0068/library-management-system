from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import *

# HOME PAGE
def index(request):
    
    return render(request, 'index.html')

# LOGIN PAGE
def login(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            return redirect('dashboard')

        else:

            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')

# REGISTER PAGe
def register(request):

    return render(request, 'register.html')

# ADMIN DASHBOARD
def dashboard(request):

    total_books = Book.objects.count()
    active_borrows = Transaction.objects.filter(is_returned=False).count()
    active_students = Student.objects.count()
    overdue_fines = Fine.objects.filter(paid=False).count()
    overdue_books = Transaction.objects.filter(is_returned=False)[:2]
    recent_activity = Transaction.objects.order_by('-borrowed_date')[:3]

    context = {
        'total_books':total_books,
        'active_borrows':active_borrows,
        'active_students':active_students,
        'overdue_fines':overdue_fines,
        'overdue_books':overdue_books,
        'recent_activity':recent_activity,
    }

    return render(
        request, 'admindashboard.html', context
    )

# STUDENT
def students(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(active=True).count()

    context = {
        'students': Student.objects.all(),
        'total_students': total_students,
        'active_students': active_students,
    }

    return render(request, 'students.html', context)

#  BOOK
def books(request):
    total_books = Book.objects.count()
    available_books = Book.objects.filter(available=True).count()
    issued_books = Transaction.objects.filter(is_returned=False).count()

    context = {
        'books':Book.objects.all(),
        'total_books':total_books,
        'available_books':available_books,
        'issued_books':issued_books
    }

    return render(request, 'books.html', context)

# TRANSACTION
def transactions(request):
    transactions = Transaction.objects.all()
    total_transactions = Transaction.objects.count()
    returned_books = Transaction.objects.filter(is_returned=True).count()
    pending_returns = Transaction.objects.filter(is_returned=False).count()

    context = {
        'transactions': transactions,
        'total_transactions': total_transactions,
        'returned_books': returned_books,
        'pending_returns': pending_returns,
    }

    return render(
        request,
        'transactions.html',
        context
    )

# FINE
from django.db.models import Sum
def fines(request):
    fines = Fine.objects.all()
    total_fines = Fine.objects.aggregate(total=Sum('amount'))['total'] or 0
    paid_fines = Fine.objects.filter(paid=True).aggregate(total=Sum('amount'))['total'] or 0
    pending_fines = Fine.objects.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'fines': fines,
        'total_fines': total_fines,
        'paid_fines': paid_fines,
        'pending_fines': pending_fines,
    }

    return render(
        request,
        'fines.html',
        context
    )


def add_student(request):
    if request.method == "POST":
        Student.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            department=request.POST['department'],
            active=request.POST['active'] == "True"
        )
        return redirect('add_student')

    students = Student.objects.all()

    return render(
        request,
        'add_student.html',
        {
            'students': students
        }
    )


def add_book(request):
    if request.method == "POST":
        Book.objects.create(
            title=request.POST['title'],
            author=request.POST['author'],
            category=request.POST['category'],
            isbn=request.POST['isbn'],
            quantity=request.POST['quantity'],
            available=request.POST['available'] == "True"
        )
        return redirect('add_book')

    books = Book.objects.all()

    return render(
        request,
        'add_book.html',
        {
            'books': books
        }
    )


def issue_book(request):
    if request.method == "POST":
        Transaction.objects.create(
            student_id=request.POST['student'],
            book_id=request.POST['book'],
            borrowed_date=request.POST['borrowed_date'],
            return_date=request.POST['return_date'],
            is_returned=request.POST['is_returned'] == "True"
        )
        return redirect('issue_book')

    context = {
        'students': Student.objects.all(),
        'books': Book.objects.filter(available=True),
        'transactions': Transaction.objects.all()
    }

    return render(
        request,
        'issue_book.html',
        context
    )

def add_fine(request):
    if request.method == "POST":
        Fine.objects.create(
            student_id=request.POST['student'],
            amount=request.POST['amount'],
            date=request.POST['date'],
            paid=request.POST['paid'] == "True"
        )
        return redirect('add_fine')

    context = {
        'students': Student.objects.all(),
        'fines': Fine.objects.all(),
    }

    return render(
        request,
        'add_fine.html',
        context
    )
