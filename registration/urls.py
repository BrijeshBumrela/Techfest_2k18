from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "registration"

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('login', auth_views.login, name="login"),
    path('logout', views.logout_view, name="logout"),
]
