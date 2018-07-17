from django.shortcuts import render
from rest_framework.generics import ListAPIView
from api.serializers import EventSerializer
from data.models import Event

class EventsList(ListAPIView):
    queryset = Event.objects.all().order_by('end_date_time', 'start_date_time')
    serializer_class = EventSerializer

