from django.db import models
from django.dispatch import receiver
import django.db.models.signals as signals

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
                                  validators=[secret_key_min_length], blank=True)
    profile_pic = models.ImageField(verbose_name="Profile Picture", upload_to=get_profilepic_upload_url, blank=True,
                                    help_text="Please upload a Profile Picture")
    description = models.TextField(verbose_name="About You", blank=True, help_text="Write A Few Lines About Yourself")
    college_name = models.CharField(verbose_name="College Name", max_length=100)
    github_id = models.CharField(verbose_name="Github Username", max_length=50, blank=True)
    hackerrank_id = models.CharField(verbose_name="Hackerrank Username", max_length=50, blank=True)
    codechef_id = models.CharField(verbose_name="Codechef Username", max_length=50, blank=True)
    codeforces_id = models.CharField(verbose_name="Codeforces Username", max_length=50, blank=True)

    def __str__(self):
        return self.user.username


@receiver(signals.post_delete, sender=MoreUserData)
def delete_profile_pic_on_model_delete(sender, instance, **kwargs):
    """
    Deletes Profile Pic from the file system once that user is deleted
    :param sender: Sender Model = MoreUserData
    :param instance: particular instance of Model
    :param kwargs: Handled by decorator
    :return:
    """
    if str(instance.profile_pic) != '':
        if os.path.isfile(instance.profile_pic.path):
            os.remove(instance.profile_pic.path)


def get_event_logo_upload_url(instance, filename):
    location = "events"
    return os.path.join(location, str(instance.name), "logos", "logo.png")


class Event(models.Model):
    name = models.CharField(verbose_name="Event Name", max_length=50, unique=True)
    logo = models.ImageField(verbose_name="Event Logo", upload_to=get_event_logo_upload_url, blank=True,
                             help_text="Please Upload A Logo For This Event")
    start_date_time = models.DateTimeField(verbose_name="Event Starts On (IST) ", )
    end_date_time = models.DateTimeField(verbose_name="Event Concludes On (IST)")
    description = models.TextField(verbose_name="Description")
    rules = models.TextField(verbose_name="Contest Rules")
    prize = models.TextField(verbose_name="Prize Description")
    organisers = models.ManyToManyField(to=MoreUserData, related_name="organising_events", blank=False,
                                        help_text="Please Select 1 or more users as Organisers")
    participants = models.ManyToManyField(to=MoreUserData, related_name="participating_events", blank=True, )

    priority = models.IntegerField(verbose_name="Priority", default=0,
                                   help_text="Events will be ordered Based on priority. Higher Priority events appear first in list")

    class Meta:
        ordering = ['-priority']

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def get_event_catalogue_upload_url(instance, filename):
    return os.path.join("events", instance.event.name, "catalogue", filename)


class EventCatalogue(models.Model):
    event = models.OneToOneField(to=Event, primary_key=True, on_delete=models.CASCADE)
    image1 = models.ImageField(verbose_name="Image 1", upload_to=get_event_catalogue_upload_url, blank=True,
                               help_text="Upload Image 1 for this Event. (optional). This is primary image that will appear on main page")
    image2 = models.ImageField(verbose_name="Image 2", upload_to=get_event_catalogue_upload_url, blank=True,
                               help_text="Upload Image 1 for this Event. (optional)")
    image3 = models.ImageField(verbose_name="Image 3", upload_to=get_event_catalogue_upload_url, blank=True,
                               help_text="Upload Image 1 for this Event. (optional)")
    image4 = models.ImageField(verbose_name="Image 4", upload_to=get_event_catalogue_upload_url, blank=True,
                               help_text="Upload Image 1 for this Event. (optional)")
    image5 = models.ImageField(verbose_name="Image 5", upload_to=get_event_catalogue_upload_url, blank=True,
                               help_text="Upload Image 1 for this Event. (optional)")
    image6 = models.ImageField(verbose_name="Image 6", upload_to=get_event_catalogue_upload_url, blank=True,
                               help_text="Upload Image 1 for this Event. (optional)")

    class Meta:
        ordering = ['-event']

    def __str__(self):
        return self.event.name + "Catalogue"
