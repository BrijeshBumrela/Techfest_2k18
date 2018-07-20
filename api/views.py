from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from api.serializers import EventSerializer, MoreUserDataSerializer
from data.models import Event, MoreUserData

class EventsList(ListAPIView):
    queryset = Event.objects.all().order_by('end_date_time', 'start_date_time')
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)


class MoreUserDataView(APIView):
    
    def get(self, request, format=None):
        user_data = request.user.moreuserdata
        serializer = MoreUserDataSerializer(user_data)
        return Response(serializer.data)
 

class RegisteredOrNotView(APIView):
    def get(self, request, format=None):
        obj = get_object_or_404(Event, id=request.GET.get('id'))
        user_data = request.user.moreuserdata
        if user_data in obj.participants.all():
            return Response({
                "participating": 1
            })
        else:
            return Response({
                "participating": 0
            })

    def post(self, request, format=None):
        obj = get_object_or_404(Event, id=request.data.get('id'))
        user_data = request.user.moreuserdata
        if user_data not in obj.participants.all():
            obj.participants.add(user_data)
        return Response(status=200)

    
