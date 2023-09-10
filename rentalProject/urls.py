"""
URL configuration for rentalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from iha import views


router = DefaultRouter()
router.register(r'ihalar', views.IHAViewSet)
router.register(r'kiralama', views.KiralamaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    #path('accounts/', include('accounts.urls')),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('iha-lists/', views.iha_lists, name='iha-lists'),
    path('iha-details/<int:iha_id>/', views.iha_details, name='iha-details'),
    path('iha_rental/<int:iha_id>/', views.iha_rental,name='iha_rental'),

    path('add_iha/', views.add_iha, name='add_iha'),
    path("delete_iha/<int:iha_id>/", views.delete_iha, name="delete_iha"),
    path("edit_iha/<int:iha_id>/", views.edit_iha, name="edit_iha"),

    path('delete_rental/<int:kiralama_id>/', views.delete_rental, name='delete_kiralama'),
    path('edit_rental/<int:kiralama_id>/', views.edit_rental, name='edit_kiralama'),
    path('orders/<int:user_id>/', views.orders, name='orders'),

    path('kiralama_sayfasi/<int:iha_id>/', views.kiralama_sayfasi, name='kiralama_sayfasi'),

]