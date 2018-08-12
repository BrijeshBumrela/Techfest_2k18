from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import *
from api.serializers import EventSerializer, MoreUserDataSerializer, UserSerializer, GoogleUserSerializer
from data.models import Event, MoreUserData
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
import os, binascii, hashlib, base64

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

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


class GoogleLogin(APIView):
    permission_classes = (AllowAny, )
    
    @transaction.atomic 
    def post(self, request, format=None):
        # if user is already created, we return JWT token, else create the user and return JWT token.
        print(request.data)
        if(request.data.get("username") and request.data.get("google_id")):
            try:
                user = User.objects.get(username=request.data.get("username"))
                # salt =  base64.decodestring(user.moreuserdata.google_salt)
                salt = str.encode(user.moreuserdata.google_salt)
                print(salt)
                google_id = request.data.get("google_id")
                print(binascii.hexlify(hashlib.pbkdf2_hmac('sha256', str(google_id).encode('utf-8'), salt, 100000)))
                print(user.moreuserdata.google_id)
                if str(binascii.hexlify(hashlib.pbkdf2_hmac('sha256', str(google_id).encode('utf-8'), salt, 100000))) == user.moreuserdata.google_id:
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    return Response({"token": token}, status=HTTP_200_OK) 
            except Exception as e:
                print(e)
            return Response({
                    "non_field_errors": [
                        "Unable to log in with provided credentials."
                    ]
                }, status=HTTP_400_BAD_REQUEST)
        serializer = GoogleUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            google_user = serializer.instance
            payload = jwt_payload_handler(google_user.user)
            token = jwt_encode_handler(payload)
            return Response({"token": token}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_409_CONFLICT)
