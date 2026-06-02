from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('students/', views.students, name='students'),
    path('add-student/', views.add_student, name='add_student'),

    path('books/', views.books, name='books'),
    path('add-book/', views.add_book, name='add_book'),

    path('transactions/', views.transactions, name='transactions'),
    path('issue-book/', views.issue_book, name='issue_book'),

    path('fines/', views.fines, name='fines'),
    path('add-fine/', views.add_fine, name='add_fine'),
]