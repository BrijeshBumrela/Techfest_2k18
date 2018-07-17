from data.models import Event
from rest_framework.serializers import ModelSerializer

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
