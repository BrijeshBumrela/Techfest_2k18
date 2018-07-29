from django import forms

from .models import Event, MoreUserData, Notification
from django.contrib.auth.models import User


class BriefEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date_time', 'end_date_time']


class DetailedEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'logo', 'description', 'start_date_time', 'end_date_time', 'rules', 'prize']


class EditProfileUserInfo(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class EditProfileMoreUserDataInfo(forms.ModelForm):
    class Meta:
        model = MoreUserData
        fields = ['profile_pic', 'college_name', 'country_code', 'phone_number', 'description', 'github_id',
                  'hackerrank_id', 'codechef_id', 'codeforces_id', 'tshirt_size']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(),required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(), min_length=8)


class UpdateTemplateForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['heading', 'content', 'button1_title', 'button1_url', 'button2_title', 'button2_url']
