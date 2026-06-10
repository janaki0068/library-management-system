from django.contrib import admin
from .models import *


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'phone',
        'department',
        'active'
    )

    search_fields = (
        'name',
        'email'
    )

    list_filter = (
        'department',
        'active'
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'category',
        'isbn',
        'quantity',
        'available'
    )

    search_fields = (
        'title',
        'author',
        'isbn'
    )

    list_filter = (
        'category',
        'available'
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'student',
        'book',
        'borrowed_date',
        'return_date',
        'is_returned'
    )

    list_filter = (
        'is_returned',
    )


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'get_student',
        'get_book',
        'amount',
        'paid'
    )

    list_filter = (
        'paid',
    )

    def get_student(self, obj):
        return obj.issue.student.username

    get_student.short_description = 'Student'

    def get_book(self, obj):
        return obj.issue.book.title

    get_book.short_description = 'Book'