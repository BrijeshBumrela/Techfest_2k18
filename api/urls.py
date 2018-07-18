from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import EventsList

app_name = "api"

urlpatterns = [
    path('api-token-auth', obtain_jwt_token),
    path('EventsList', EventsList.as_view(), name="EventsList"),
]
