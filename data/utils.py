
from . import models

from django.contrib.auth.models import User

from django.db import IntegrityError
from django.utils import timezone

from accounts.views import MD5encrypt


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
            event = models.Event(name="Sample Event " + str(i),
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


def create_validated_user(**kwargs):
    if 'username' not in kwargs:
        print("username:", end=' ')
        kwargs['username'] = input()

    if 'email' not in kwargs:
        print("email:", end=' ')
        kwargs['email'] = input()

    if 'password' not in kwargs:
        print("password:", end=' ')
        kwargs['password'] = input()

    if 'first_name' not in kwargs:
        print("First Name:", end=' ')
        kwargs['first_name'] = input()

    if 'last_name' not in kwargs:
        print("Last Name:", end=' ')
        kwargs['last_name'] = input()

    if 'college_name' not in kwargs:
        kwargs['college_name'] = 'Indian Institute Of Information Technology, Sri City'

    U = User.objects.create_user(username=kwargs['username'],
                                 password=kwargs['password'],
                                 email=kwargs['email'],
                                 )

    U.first_name = kwargs['first_name']
    U.last_name = kwargs['last_name']

    U.emailconfirmation.email_confirmed = True

    U.save()

    MU = models.MoreUserData(user=U, college_name=kwargs["college_name"])
    if 'ph_no' in kwargs:
        MU.phone_number = kwargs['ph_no']
    MU.secret_key = MD5encrypt(U.username)
    MU.save()

