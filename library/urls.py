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
    path('update-student/<int:id>/',views.update_student,name='update_student'),

    path('books/', views.books, name='books'),
    path('add-book/', views.add_book, name='add_book'),
    path('books/delete/<int:id>/', views.delete_book, name='delete_book'),
    path('books-update/<int:id>/', views.update_book, name='update_book'),

    path('transactions/', views.transactions, name='transactions'),
    path('issue-book/', views.issue_book, name='issue_book'),
    path('transactions/delete/<int:id>/',views.delete_transaction,name='delete_transaction'),

    path('fines/', views.fines, name='fines'),
    path('add-fine/', views.add_fine, name='add_fine'),
    path('delete-fine/<int:id>/',views.delete_fine,name='delete_fine'),

    path('categories/', views.categories, name='categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('delete-category/<int:id>/',views.delete_category,name='delete_category'),

    path('request-borrow/<int:book_id>/',views.request_borrow,name='request_borrow'),

    path('borrow-requests/',views.borrow_requests,name='borrow_requests'),
    path('approve-request/<int:request_id>/',views.approve_request,name='approve_request'),
    path('reject-request/<int:request_id>/',views.reject_request,name='reject_request'),
    path('return-book/<int:issue_id>/',views.return_book,name='return_book'),

    path('user-fines/',views.user_fines,name='user_fines'),
]
