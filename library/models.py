from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# STUDENT MODEL
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, default='')
    department = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    student_id = models.CharField(max_length=20, unique=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    
# BOOK MODEL
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    isbn = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )
    quantity = models.IntegerField(default=1)
    available = models.BooleanField(default=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    def __str__(self):
        return self.title


# TRANSACTION MODEL
class Transaction(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    borrowed_date = models.DateField(
        auto_now_add=True
    )

    return_date = models.DateField(
        null=True,
        blank=True
    )

    is_returned = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.student} borrowed {self.book}"


# FINE MODEL
class Fine(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    paid = models.BooleanField(
        default=False
    )

    date = models.DateField(
        default=timezone.now
    )

    def __str__(self):
        return f"{self.student} - {self.amount}"
    