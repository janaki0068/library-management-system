from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('browse-books/', views.browse_books, name='browse_books'),
]