from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
import main_page.views

app_name = "registration"

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('login', auth_views.login, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('account-activation-email-sent', views.account_activation_email_sent, name='account_activation_email_sent'),
    path('activate/<uidb64>/<token>', main_page.views.redirect_to_index, name='activate'),
    path('send_activation_mail', views.send_account_activation_email)
]
