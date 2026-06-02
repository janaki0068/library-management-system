from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum

from .models import *


# HOME PAGE

def index(request):
    return render(request, 'index.html')


# LOGIN

def login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            if user.is_staff:
                return redirect('dashboard')

            return redirect('dashboard')

        return render(
            request,
            'login.html',
            {
                'error': 'Invalid username or password'
            }
        )

    return render(request, 'login.html')


# REGISTER

def register(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match'
            )

            return render(
                request,
                'register.html'
            )

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists'
            )

            return render(
                request,
                'register.html'
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(
        request,
        'register.html'
    )


# LOGOUT

def logout(request):

    auth_logout(request)

    return redirect('index')


# DASHBOARD

def dashboard(request):

    total_books = Book.objects.count()

    active_borrows = Transaction.objects.filter(
        is_returned=False
    ).count()

    active_students = Student.objects.filter(
        active=True
    ).count()

    overdue_fines = Fine.objects.filter(
        paid=False
    ).count()

    overdue_books = Transaction.objects.filter(
        is_returned=False
    )[:5]

    recent_activity = Transaction.objects.order_by(
        '-borrowed_date'
    )[:5]

    context = {
        'total_books': total_books,
        'active_borrows': active_borrows,
        'active_students': active_students,
        'overdue_fines': overdue_fines,
        'overdue_books': overdue_books,
        'recent_activity': recent_activity,
    }

    return render(
        request,
        'admindashboard.html',
        context
    )


# STUDENTS

def students(request):

    total_students = Student.objects.count()

    active_students = Student.objects.filter(
        active=True
    ).count()

    context = {
        'students': Student.objects.all(),
        'total_students': total_students,
        'active_students': active_students,
    }

    return render(
        request,
        'students.html',
        context
    )


# ADD STUDENT

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

    context = {
        'students': Student.objects.all()
    }

    return render(
        request,
        'add_student.html',
        context
    )


# BOOKS

def books(request):

    total_books = Book.objects.count()

    available_books = Book.objects.filter(
        available=True
    ).count()

    issued_books = Transaction.objects.filter(
        is_returned=False
    ).count()

    context = {
        'books': Book.objects.all(),
        'total_books': total_books,
        'available_books': available_books,
        'issued_books': issued_books,
    }

    return render(
        request,
        'books.html',
        context
    )


# ADD BOOK

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

    context = {
        'books': Book.objects.all()
    }

    return render(
        request,
        'add_book.html',
        context
    )


# TRANSACTIONS

def transactions(request):

    transactions = Transaction.objects.all()

    total_transactions = Transaction.objects.count()

    returned_books = Transaction.objects.filter(
        is_returned=True
    ).count()

    pending_returns = Transaction.objects.filter(
        is_returned=False
    ).count()

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


# ISSUE BOOK

def issue_book(request):

    if request.method == "POST":

        book = Book.objects.get(
            id=request.POST['book']
        )

        Transaction.objects.create(
            student_id=request.POST['student'],
            book=book,
            borrowed_date=request.POST['borrowed_date'],
            return_date=request.POST['return_date'],
            is_returned=False
        )

        book.available = False
        book.save()

        return redirect('issue_book')

    context = {
        'students': Student.objects.all(),
        'books': Book.objects.filter(
            available=True
        ),
        'transactions': Transaction.objects.all(),
    }

    return render(
        request,
        'issue_book.html',
        context
    )


# FINES

def fines(request):

    fines = Fine.objects.all()

    total_fines = Fine.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    paid_fines = Fine.objects.filter(
        paid=True
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    pending_fines = Fine.objects.filter(
        paid=False
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

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


# ADD FINE

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