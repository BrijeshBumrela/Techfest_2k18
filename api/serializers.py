from data.models import Event, MoreUserData
from django.contrib.auth.models import User
from rest_framework import serializers 
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

class MoreUserDataSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = MoreUserData
        exclude = ('secret_key',)
    
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)
        user.set_password(user_data["password"])
        user.save()
        more_user_data = MoreUserData()
        more_user_data.user = user
        more_user_data.college_name = validated_data.pop("college_name")
        more_user_data.save()
        return more_user_data

class UserSerializer2(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')

class MoreUserDataSerializer2(ModelSerializer):
    user = UserSerializer2()
    class Meta:
        model = MoreUserData
        fields = ('user',)

class EventSerializer(ModelSerializer):
    participants = MoreUserDataSerializer2(many=True)
    organisers = MoreUserDataSerializer2(many=True)
    class Meta:
        model = Event
        fields = '__all__'
