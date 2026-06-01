from time import timezone

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *

# HOME PAGE


def index(request):

    return render(request, 'index.html')

# LOGIN PAGE


def login(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') 

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            if not remember_me:
                request.session.set_expiry(0)       #expires when browser closes
            else:
                request.session.set_expiry(86400 * 7)       #expires in 7 days

            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('user_dashboard')

        else:

            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')

# REGISTER PAGe


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        student_id = request.POST.get('student_id')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')

        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        if role == 'admin':
            user.is_staff = True
            user.save()

        Student.objects.create(
            user=user,
            student_id=student_id,
            phone=phone,
            date_of_birth=dob if dob else None
        )

        messages.success(request, 'Account created successfully')
        return redirect('login')

    return render(request, 'register.html')

def forgot_password(request):
    return render(request, 'forgotpassword.html')

# LOGOUT PAGE


def logout(request):
    auth_logout(request)
    return redirect('index')

# ADMIN DASHBOARD


def dashboard(request):

    total_books = Book.objects.count()
    active_borrows = Transaction.objects.filter(is_returned=False).count()
    active_students = Student.objects.count()
    overdue_fines = Fine.objects.filter(paid=False).count()
    overdue_books = Transaction.objects.filter(is_returned=False)[:2]
    recent_activity = Transaction.objects.order_by('-borrowed_date')[:3]

    context = {
        'total_books': total_books,
        'active_borrows': active_borrows,
        'active_students': active_students,
        'overdue_fines': overdue_fines,
        'overdue_books': overdue_books,
        'recent_activity': recent_activity,
    }

    return render(
        request, 'admindashboard.html', context
    )

# user dashboard


@login_required
def user_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        borrowed_books = Transaction.objects.filter(
            student=student, is_returned=False).count()
        returned_books = Transaction.objects.filter(
            student=student, is_returned=True).count()
        fines = Fine.objects.filter(student=student, paid=False)
        total_fines = sum(fine.amount for fine in fines)
    except Student.DoesNotExist:
        student = None
        borrowed_books = returned_books = total_fines = 0

    context = {
        'student': student,
        'borrowed_books': borrowed_books,
        'returned_books': returned_books,
        'total_fines': total_fines,
    }

    return render(request, 'userdashboard.html', context)


@login_required
def profile_picture(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        if request.FILES.get('profile_picture'):
            student.profile_picture = request.FILES['profile_picture']
            student.save()
    return redirect('user_dashboard')


@login_required
def browse_books(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query) | books.filter(
            author__icontains=query)

    if category:
        books = books.filter(category__icontains=category)

    categories = Book.objects.exclude(category='').values_list('category', flat=True).distinct()

    context = {
        'books': books,
        'query': query,
        'selected_category': category,
        'categories': categories,
    }

    return render(request, 'browsebooks.html', context)


@login_required
def user_books(request):
    try:
        student = Student.objects.get(user=request.user)
        transactions = Transaction.objects.filter(
            student=student, is_returned=False)

        today = timezone.now().date()
        for t in transactions:
            if t.return_date:
                if t.return_date < today:
                    t.status = 'overdue'
                elif t.due_date - today <= timezone.timedelta(days=3):
                    t.status = 'due_soon'
                else:
                    t.status = 'active'
            else:
                t.status = 'active'

    except Student.DoesNotExist:
        transactions = []

    context = {
        'transactions': transactions,
    }

    return render(request, 'userbooks.html', context)


@login_required
def user_fines(request):
    try:
        student = Student.objects.get(user=request.user)
        fines = Fine.objects.filter(student=student, paid=False)
        total_fines = sum(fine.amount for fine in fines)
    except Student.DoesNotExist:
        fines = []
        total_fines = 0

    context = {
        'fines': fines,
        'total_fines': total_fines,
    }

    return render(request, 'userfines.html', context)
