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

# user dashboard
def user_dashboard(request):

    return render(request, 'userdashboard.html')

def browse_books(request):

    books = Book.objects.all()

    return render(request, 'browsebooks.html', {'books': books})