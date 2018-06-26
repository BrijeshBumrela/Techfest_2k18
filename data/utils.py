
from . import models

from django.contrib.auth.models import User

from django.db import IntegrityError
from django.utils import timezone


# Create your tests here.

def create_users(number_of_users=10):
    """Creates Users"""

    for i in range(number_of_users):
        try:
            U = User.objects.create_user(username="testuser" + str(i),
                                         password="testuser" + str(i),
                                         email="testuser" + str(i) + "@testusers.com"
                                         )
        except IntegrityError:
            continue
        MU = models.MoreUserData(user=U, college_name="BlahBlah", github_id="testuser" + str(i))
        MU.save()


def create_events(number_of_events=10):
    """Creates Sample Events"""
    for i in range(number_of_events):
        try:
            event = models.Event(name="Sample Event" + str(i),
                                 start_date_time=timezone.now(),
                                 end_date_time=timezone.now(),
                                 description="Sample Event",
                                 rules="Sample Event",
                                 prize="Sample Event",
                                 )
            event.save()
        except IntegrityError:
            continue

        try:
            event.organisers.add(models.MoreUserData.objects.all()[0])
        except IndexError:
            raise IndexError("Create at least 1 user before creating events")

