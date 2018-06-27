from django import forms
from django.contrib.auth.models import User
import data.models


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class MoreUserDataForm(forms.ModelForm):
    class Meta:
        model = data.models.MoreUserData
        fields = ['profile_pic', 'college_name', 'github_id', 'hackerrank_id', 'codechef_id', 'codeforces_id',
                  'description']
