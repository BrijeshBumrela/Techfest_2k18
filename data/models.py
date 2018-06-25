from django.db import models

from django.contrib.auth.models import User

import os.path
from django.core.validators import MaxLengthValidator, MinLengthValidator


# Create your models here.
def get_profilepic_upload_url(instance, filename):
    location = "profile_pictures"
    return os.path.join(location, str(instance.user.id))


class MoreUserData(models.Model):
    user = models.OneToOneField(to=User, primary_key=True, on_delete=models.CASCADE)
    secret_key_length = 32
    secret_key_min_length = MinLengthValidator(secret_key_length)
    secret_key = models.CharField(verbose_name="Secret Key", max_length=secret_key_length,
                                  validators=[secret_key_min_length],blank=True)
    profile_pic = models.ImageField(verbose_name="Profile Picture", upload_to=get_profilepic_upload_url, blank=True,
                                    help_text="Please upload a Profile Picture")
    college_name = models.CharField(verbose_name="College Name", max_length=100)
    github_id = models.CharField(verbose_name="Github Username", max_length=50, blank=True)
    hackerrank_id = models.CharField(verbose_name="Hackerrank Username", max_length=50, blank=True)
    codechef_id = models.CharField(verbose_name="Codechef Username", max_length=50, blank=True)
    codeforces_id = models.CharField(verbose_name="Codeforces Username", max_length=50, blank=True)
