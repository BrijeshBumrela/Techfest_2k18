from django import forms


class EventRegisterForm(forms.Form) :
    username = forms.CharField(widget=forms.HiddenInput())
    event = forms.CharField(widget=forms.HiddenInput())
