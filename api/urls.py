from django.urls import path
from .views import EventsList

app_name = "api"

urlpatterns = [
    path('EventsList', EventsList.as_view(), name="EventsList"),
]
