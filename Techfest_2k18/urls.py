"""Techfest_2k18 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include, re_path
import main_page.views
from . import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', main_page.views.index),
    path('', main_page.views.redirect_to_index, name="home"),
    path('events', main_page.views.display_events, name="events"),
    path('event/<slug:event_name>', main_page.views.event_info, name="event info"),
    path('registration/', include('registration.urls')),
    path('accounts/', include('accounts.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('password_reset/', auth_views.password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    path('reset/(<uidb64>/<token>', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
    path('contact-us', main_page.views.contact_us, name="contact_us"),
    # ----
    # TEMPORARY
    path('tempeventinfo', main_page.views.temp_event_info),
    # ------

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
