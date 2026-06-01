from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('browse-books/', views.browse_books, name='browse_books'),
    path('user-books/', views.user_books, name='user_books'),
    path('user-fines/', views.user_fines, name='user_fines'),
    path('profile-picture/', views.profile_picture, name='profile_picture'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]