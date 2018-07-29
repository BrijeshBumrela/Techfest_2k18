from django.db import models
from django.dispatch import receiver
import django.db.models.signals as signals

from django.contrib.auth.models import User

import os.path
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError

from django.shortcuts import reverse


# Create your models here.

class EmailConfirmation(models.Model):
    user = models.OneToOneField(to=User, primary_key=True, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(signals.post_save, sender=User)
def put_email_confirmed_false(sender, instance, created, **kwargs):
    if created:
        EmailConfirmation.objects.create(user=instance)
        if instance.has_usable_password() is False:
            # Users passing through oauth don't need to confirm email
            instance.emailconfirmation.email_confirmed = True

        elif instance.is_superuser:
            # Superusers don't need to confirm emails
            instance.emailconfirmation.email_confirmed = True

    instance.emailconfirmation.save()


def get_profilepic_upload_url(instance, filename):
    location = "profile_pictures"
    return os.path.join(location, str(instance.user.id), filename)


class MoreUserData(models.Model):
    COUNTRY_CODE_CHOICES = (
        ('+91', 'India(+91)'),
        ('+7', 'Russia(+7)'),
        ('+81', 'Japan(+81)'),
        ('+1', 'USA(+1)'),
        ('+972', 'Israel(+972)')
    )
    TSHIRT_SIZE_CHOICES = (
        ('S', 'Small(S)'),
        ('M', 'Medium(M)'),
        ('L', 'Large(L)'),
        ('XL', 'Extra Large(XL)'),
        ('XXL', 'Extra Extra Large(XXL)')
    )
    COLLEGE_CHOICES = ()
    user = models.OneToOneField(to=User, primary_key=True, on_delete=models.CASCADE)
    secret_key_length = 32
    secret_key_min_length = MinLengthValidator(secret_key_length)
    secret_key = models.CharField(verbose_name="Secret Key", max_length=secret_key_length,
                                  validators=[secret_key_min_length], blank=True)
    profile_pic = models.ImageField(verbose_name="Profile Picture", upload_to=get_profilepic_upload_url, blank=True,
                                    help_text="Please upload a Profile Picture")
    country_code = models.CharField(verbose_name="Country Code for Phone Number", max_length=4,
                                    choices=COUNTRY_CODE_CHOICES,
                                    default='+91')
    phone_number = models.CharField(verbose_name="Phone Number", max_length=10, validators=[MinLengthValidator(10)],
                                    blank=True)
    college_name = models.CharField(verbose_name="College Name", max_length=100)
    description = models.TextField(verbose_name="About You", blank=True, help_text="Write A Few Lines About Yourself")
    tshirt_size = models.CharField(verbose_name="T-Shirt Size", max_length=3, blank=True, choices=TSHIRT_SIZE_CHOICES,
                                   help_text="Enter your T shirt size so that we can get you one if you win")

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
    return os.path.join(location, str(instance.name), "logos", filename)


def event_name_slug_validator(event_name):
    if '-' in str(event_name):
        raise ValidationError("- not Allowed in event name as they will clash with event name slug")


class Event(models.Model):
    name = models.CharField(verbose_name="Event Name", max_length=50, unique=True,
                            validators=[event_name_slug_validator],
                            help_text="All characters allowed except '-' as this may collide with slug of event name")
    logo = models.ImageField(verbose_name="Event Logo", upload_to=get_event_logo_upload_url, blank=True,
                             help_text="Please Upload A Logo For This Event")
    registration_start_date_time = models.DateTimeField(verbose_name="Registration Starts On (IST) ", )
    registration_end_date_time = models.DateTimeField(verbose_name="Registration Ends On (IST) ", )
    start_date_time = models.DateTimeField(verbose_name="Event Starts On (IST) ", )
    end_date_time = models.DateTimeField(verbose_name="Event Concludes On (IST)")
    description = models.TextField(verbose_name="Description", blank=True, max_length=1500,
                                   help_text="Formatting Enabled. Seperate different sections using '***'. Encase headings between ___Heading___ . Seperate different lines using '&#92;n'")
    format = models.TextField(verbose_name="Format", blank=True, max_length=1500)
    rules = models.TextField(verbose_name="Contest Rules", blank=True, max_length=1500)
    prize = models.TextField(verbose_name="Prize Description", blank=True, max_length=1000)
    prerequisites = models.TextField(verbose_name="Pre-Requisites", blank=True, max_length=1000)
    resources = models.TextField(verbose_name="Resources", blank=True, max_length=1500)
    organisers = models.ManyToManyField(to=MoreUserData, related_name="organising_events", blank=True,
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
        ordering = ['event']

    def __str__(self):
        return self.event.name + " Catalogue"


class EventCatagory(models.Model):
    name = models.CharField(verbose_name="Catagory Name", max_length=15)
    events = models.ManyToManyField(to=Event, verbose_name="Events belonging to this catagory", blank=True, related_name="catagories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)


def get_committee_upload_url(instance, filename):
    return os.path.join("committee", instance.name, "logo" + filename)


class Committee(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(to=MoreUserData, blank=True)
    committee_lgo = models.ImageField(verbose_name="Committee Logo", upload_to=get_committee_upload_url, blank=True)

    def __str__(self):
        return self.name


def phone_number_validator(ph_no):
    pass


class CommitteeContactInfo(models.Model):
    committee = models.OneToOneField(to=Committee, on_delete=models.CASCADE)
    phone_number_min_length = MinLengthValidator(10)
    phone_number = models.CharField(max_length=10, validators=[phone_number_min_length], blank=True,
                                    help_text="Enter The contact number of committee without the preceeding country code")
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.committee.name


class Notification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=15, help_text="Keyword that identifies different types of updates", null=True,
                               blank=True)
    heading = models.CharField(max_length=35)
    content = models.CharField(max_length=500)
    button1 = models.CharField(max_length=500, verbose_name="Dynamic link for URLs", null=True, blank=True)
    button1_title = models.CharField(max_length=20, blank=True, null=True)
    button1_url = models.URLField(blank=True)
    button2 = models.CharField(max_length=500, verbose_name="Dynamic link for URLS", null=True, blank=True)
    button2_title = models.CharField(max_length=20, blank=True, null=True)
    button2_url = models.URLField(blank=True)

    def __str__(self):
        return self.keyword + " " + self.user.username + "" + str(self.id)

    def new_update(self, user_instance, notif_heading, notif_content, but1="", but2=""):
        self.user = user_instance
        self.heading = notif_heading
        self.content = notif_content
        self.button1 = but1
        self.button2 = but2

        self.save()

    def generate_urls(self):
        if self.button1:
            self.button1_url = reverse(self.button1)
        else:
            self.button1_url = ""

        if self.button2:
            self.button2_url = reverse(self.button2)
        else:
            self.button2_url = ""

        self.save()


@receiver(signals.post_save, sender=User)
def moreuserdata_missing_update(sender, instance, created, **kwargs):
    if created:
        n1 = Notification.objects.create(user=instance,
                                         keyword="moreuserdata_missing",
                                         heading="Missing Info",
                                         content="Your Profile Is missing some important information. You can not register for events until the information is filled",
                                         button1='accounts:edit_additional_info',
                                         button1_title="Fill Missing Info"
                                         )


@receiver(signals.post_save, sender=MoreUserData)
def remove_moreuserdata_missing_update(sender, instance, created, **kwargs):
    if created:
        instance.user.notification_set.filter(keyword='moreuserdata_missing').delete()
