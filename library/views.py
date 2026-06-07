from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if not remember_me:
                request.session.set_expiry(0)

            else:
                request.session.set_expiry(86400 * 7)

            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('user_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


# REGISTER
def register(request):
    if request.method == "POST":
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

    return render(
        request,
        'register.html'
    )


# LOGOUT
def logout(request):

    auth_logout(request)

    return redirect('index')


def forgot_password(request):

    return render(request, 'forgot_password.html')


# DASHBOARD
def dashboard(request):
    total_books = Book.objects.count()
    active_borrows = Transaction.objects.filter(is_returned=False).count()
    active_students = Student.objects.filter(active=True).count()
    overdue_fines = Fine.objects.filter(paid=False).count()
    overdue_books = Transaction.objects.filter(is_returned=False)[:5]
    recent_activity = Transaction.objects.order_by('-borrowed_date')[:5]

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

    categories = Book.objects.exclude(category='').values_list(
            'category', flat=True).distinct()

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

                elif t.return_date - today <= timezone.timedelta(days=3):

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

# STUDENTS
def students(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(active=True).count()
    inactive_students = Student.objects.filter(active=False).count()

    context = {
        'active_page': 'students',
        'students': Student.objects.all(),
        'total_students': total_students,
        'active_students': active_students,
        'inactive_students': inactive_students,
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

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()

    messages.success(request, "Student deleted successfully.")
    return redirect('students')


# BOOKS
def books(request):
    total_books = Book.objects.count()
    available_books = Book.objects.filter(available=True).count()
    issued_books = Transaction.objects.filter(is_returned=False).count()

    context = {
        'active_page':'books',
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

def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('books')


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

def delete_transaction(request, id):
    transaction = Transaction.objects.get(id=id)
    transaction.delete()
    return redirect('transactions')


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

        student = Student.objects.get(
            id=request.POST.get('student')
        )

        Fine.objects.create(
            student=student,
            amount=request.POST.get('amount'),
            date=request.POST.get('date'),
            paid=request.POST.get('paid') == 'True'
        )

        return redirect('fines')

    context = {
        'students': Student.objects.all(),
        'fines': Fine.objects.all()
    }

    return render(
        request,
        'add_fine.html',
        context
    )

def delete_fine(request, id):
    fine = Fine.objects.get(id=id)
    fine.delete()
    return redirect('fines')


def update_book(request, id):

    book = Book.objects.get(id=id)

    if request.method == "POST":

        book.title = request.POST['title']
        book.author = request.POST['author']
        book.category = request.POST['category']
        book.isbn = request.POST['isbn']
        book.quantity = request.POST['quantity']
        book.available = request.POST['available'] == "True"
        book.save()
        messages.success(request, "Book updated successfully.")
        return redirect('books')

    context = {
        'book': book
    }

    return render(
        request,
        'update_book.html',
        context
    )


def update_student(request, id):

    student = Student.objects.get(id=id)

    if request.method == "POST":

        student.name = request.POST['name']
        student.email = request.POST['email']
        student.phone = request.POST['phone']
        student.department = request.POST['department']
        student.active = request.POST['active'] == "True"
        student.save()
        messages.success(request, "Student updated successfully.")
        return redirect('students')

    context = {
        'student': student
    }

    return render(
        request,
        'update_student.html',
        context
    )