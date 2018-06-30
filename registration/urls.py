from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

app_name = "registration"

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('login', auth_views.login, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('account-activation-email-sent', views.account_activation_email_sent, name='account_activation_email_sent'),
    path('activate/<uidb64>/<token>', views.activate_account, name='activate'),
    path('resend-activation-link', views.generate_new_activation_link, name='resend_activation_link'),

]
