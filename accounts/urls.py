from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "accounts"

urlpatterns = [
    path('profile', views.redirect_to_profile_home, ),
    path('profile/', views.redirect_to_profile_home),
    path('profile/edit', views.edit_info, name="edit_additional_info"),
    path('profile/home', views.profile_home, name="profile_home"),
    path('updates', views.updates, name="updates"),
    path('login/', auth_views.login, name="login"),
    path('event/<slug:event_name>/register', views.register_user_for_event, name="register_for_event"),
    path('event/<slug:event_name>/deregister', views.un_register_user_for_event, name="un_register_for_event"),
    path('myevents', views.display_user_registered_events, name="myevents"),
    path('maps', views.maps, name="map"),
    path('calender', views.calender, name="calender"),
    path('password-change', views.change_password, name="change_password")
]
