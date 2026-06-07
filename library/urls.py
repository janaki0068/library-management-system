from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    path('browse-books/', views.browse_books, name='browse_books'),
    path('user-books/', views.user_books, name='user_books'),
    path('user-fines/', views.user_fines, name='user_fines'),

    path('profile_picture/', views.profile_picture, name='profile_picture'),

    path('students/', views.students, name='students'),
    path('add-student/', views.add_student, name='add_student'),
    path('delete-student/<int:student_id>/',views.delete_student,name='delete_student'),

    path('books/', views.books, name='books'),
    path('add-book/', views.add_book, name='add_book'),
    path('books/delete/<int:id>/', views.delete_book, name='delete_book'),

    path('transactions/', views.transactions, name='transactions'),
    path('issue-book/', views.issue_book, name='issue_book'),
    path('transactions/delete/<int:id>/',views.delete_transaction,name='delete_transaction'),

    path('fines/', views.fines, name='fines'),
    path('add-fine/', views.add_fine, name='add_fine'),
    path('delete-fine/<int:id>/',views.delete_fine,name='delete_fine'),

]
