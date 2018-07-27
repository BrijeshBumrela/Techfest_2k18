from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import *
from api.serializers import EventSerializer, MoreUserDataSerializer, UserSerializer
from data.models import Event, MoreUserData
from django.db import transaction

class EventsList(ListAPIView):
    queryset = Event.objects.all().order_by('end_date_time').order_by('start_date_time')
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
        add_or_remove = bool(request.data.get('add_or_remove'))
        user_data = request.user.moreuserdata
        if add_or_remove and user_data not in obj.participants.all():
            obj.participants.add(user_data)
        if not add_or_remove and user_data in obj.participants.all():
            obj.participants.remove(user_data)
        return Response(status=HTTP_200_OK)


class AllRegisteredEventsView(APIView):
    def get(self, request, format=None):
        queryset = Event.objects.filter(participants=request.user.moreuserdata).order_by('end_date_time', 'start_date_time')
        serializer = EventSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

class RegisterUserView(APIView):
    permission_classes = (AllowAny, )

    @transaction.atomic #to make sure a user is not created without more user data instance of that user
    def post(self, request, format=None):
        serializer = MoreUserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_409_CONFLICT)

