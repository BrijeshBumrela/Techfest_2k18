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
    secret_key_length = 15
    secret_key_min_length = MinLengthValidator(secret_key_length)
    secret_key = models.CharField(verbose_name="Secret Key", max_length=secret_key_length,
                                  validators=[secret_key_min_length], blank=True)
    profile_pic = models.ImageField(verbose_name="Profile Picture", upload_to=get_profilepic_upload_url, blank=True,
                                    help_text="Please upload a Profile Picture")
    description = models.TextField(verbose_name="About You", blank=True, help_text="Write A Few Lines About Yourself" )
    college_name = models.CharField(verbose_name="College Name", max_length=100)
    github_id = models.CharField(verbose_name="Github Username", max_length=50, blank=True)
    hackerrank_id = models.CharField(verbose_name="Hackerrank Username", max_length=50, blank=True)
    codechef_id = models.CharField(verbose_name="Codechef Username", max_length=50, blank=True)
    codeforces_id = models.CharField(verbose_name="Codeforces Username", max_length=50, blank=True)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    name = models.CharField(verbose_name="Event Name", max_length=50 , unique=True)
    start_date_time = models.DateTimeField(verbose_name="Event Starts On (IST) ", )
    end_date_time = models.DateTimeField(verbose_name="Event Concludes On (IST)")
    description = models.TextField(verbose_name="Description")
    rules = models.TextField(verbose_name="Contest Rules")
    prize = models.TextField(verbose_name="Prize Description")
    organisers = models.ManyToManyField(to=MoreUserData, related_name="organising_events", blank=False,
                                        help_text="Please Select 1 or more users as Organisers")
    participants = models.ManyToManyField(to=MoreUserData, related_name="participating_events", blank=True, )

    def __str__(self):
        return self.name
