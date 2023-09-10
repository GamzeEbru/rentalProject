from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name="login"), #tamam
    path('register/', views.user_register, name="register"), #tamam
    path('dashboard/', views.orders, name="dashboard"),
    path('logout/', views.user_logout, name="logout"),
    path('rent_iha/', views.rent_iha, name="enroll_the_course"),
    path('release_iha/', views.release_iha, name="release_the_course"),

]
