from django.db import models
from django.utils import timezone

# STUDENT MODEL
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, default='')
    department = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
#BOOK MODEL
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default='General')
    isbn = models.CharField(max_length=50, unique=True, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
#TRANSACTION MODEL
class Transaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} borrowed {self.book}"
    
# FINE MODEL
class Fine(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    paid = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student} - {self.amount}"