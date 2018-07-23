from data.models import Event, MoreUserData
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)

class MoreUserDataSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = MoreUserData
        exclude = ('secret_key',)

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
