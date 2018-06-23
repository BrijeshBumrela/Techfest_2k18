from django import forms

from .models import Event


class BriefEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date_time', 'end_date_time']


class DetailedEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date_time', 'end_date_time', 'rules', 'prize']
