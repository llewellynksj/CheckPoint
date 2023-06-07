from django.contrib import admin
from django.urls import path, include
from . import views
from home.views import HomeView
from .views import (index,
                    UserEditView,
                    PasswordsChangeView,
                    ShowProfilePageView,
                    EditProfilePageView)

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('newsletter/', views.newslett, name='newsletter'),
    path('validate/', views.validate_email, name='validate_email'),
    path('', index),
    path('', HomeView.as_view(), name='Home'),
    path('blog/', include('blogPoint.urls')),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('password/',
         PasswordsChangeView.as_view
         (template_name='account/password_change.html')),
    path('<int:pk>/profile',
         ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile_page',
         EditProfilePageView.as_view(), name='edit_profile_page'),
]
