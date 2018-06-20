from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "accounts"

urlpatterns = [
    path('profile', views.redirect_to_profile_home),
    path('profile/', views.redirect_to_profile_home),
    path('profile/edit-additional-info', views.edit_additional_info, name="edit_additional_info"),
    path('profile/home', views.profile_home, name="profile_home"),
    path('login/', auth_views.login, name="login")
]
