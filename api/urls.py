from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import EventsList, MoreUserDataView, RegisteredOrNotView, AllRegisteredEventsView, RegisterUserView, GoogleLogin

app_name = "api"

urlpatterns = [
    path('api-token-auth', obtain_jwt_token),
    path('EventsList', EventsList.as_view(), name="EventsList"),
    path('MoreUserDataView', MoreUserDataView.as_view(), name="MoreUserDataView"),
    path('GoogleLogin', GoogleLogin.as_view(), name="GoogleLogin"),
    path('RegisteredOrNotView', RegisteredOrNotView.as_view(), name="RegisteredOrNotView"),
    path('RegisterUserView', RegisterUserView.as_view(), name="RegisterUserView"),
    path('AllRegisteredEventsView', AllRegisteredEventsView.as_view(), name="AllRegisteredEventsView"),
]
