from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from data.models import MoreUserData, Event
from django.contrib.auth.models import User
from data.forms import EditProfileMoreUserDataInfo, EditProfileUserInfo
from django.contrib.auth.decorators import login_required
from main_page.forms import EventRegisterForm
import os.path
# For encryption
import hashlib
# The QR code file
from . import QRcode

# Create your views here.


secret_string = ''


def email_confirmation_required(func):
    """
    A decorator which allows to access url only if email for current user has been confirmed.
    THE DECORATOR login_required MUST ALWAYS PRECEDE THIS

    """
    def checker(request, *args, **kwargs):
        if request.user.emailconfirmation.email_confirmed is True:
            return func(request, *args, **kwargs)

        else:
            return render(request, "accounts/email_not_verified.html")

    return checker


def MD5encrypt(str1):
    str1 = str(str1)
    str2 = 'ksbdyemxl'
    str3 = 'snaoheiwmsceqf'
    str4 = str2 + str1 + str3

    result = hashlib.md5(str4.encode())

    return result.hexdigest()


def redirect_to_profile_home(request):
    return redirect('accounts:profile_home')


@login_required
@email_confirmation_required
def profile_home(request):
    User = {"username": request.user.username}
    additional_info_check = False

    if hasattr(request.user, 'moreuserdata'):
        additional_info_check = True
        S = str(request.user.moreuserdata.profile_pic)
        if S is not '':
            User["profile_pic"] = request.user.moreuserdata.profile_pic.url

    return render(request, "accounts/profile_home.html", {"additional_info_check": additional_info_check, "user": User})


@login_required
@email_confirmation_required
def edit_info(request):
    if request.method == "POST":

        user_data_form = EditProfileUserInfo(request.POST)
        more_user_data_form = EditProfileMoreUserDataInfo(request.POST)

        if user_data_form.is_valid():
            U = request.user
            U.first_name = user_data_form.cleaned_data['first_name']
            U.last_name = user_data_form.cleaned_data['last_name']
            U.save()

        if more_user_data_form.is_valid():

            MUD = None
            if hasattr(request.user, 'moreuserdata'):
                MUD = request.user.moreuserdata
            else:
                MUD = MoreUserData()
                MUD.user = request.user
                # Encryption
                MUD.secret_key = MD5encrypt(request.user.username)
                # Using the variable secret_string to send to qrcode
                secret_string = str(MUD.secret_key)

            MUD.college_name = more_user_data_form.cleaned_data["college_name"]
            MUD.country_code = more_user_data_form.cleaned_data["country_code"]
            MUD.phone_number = more_user_data_form.cleaned_data["phone_number"]
            MUD.description = more_user_data_form.cleaned_data["description"]
            MUD.github_id = more_user_data_form.cleaned_data["github_id"]
            MUD.hackerrank_id = more_user_data_form.cleaned_data["hackerrank_id"]
            MUD.codechef_id = more_user_data_form.cleaned_data["codechef_id"]
            MUD.codeforces_id = more_user_data_form.cleaned_data["codeforces_id"]
            MUD.tshirt_size = more_user_data_form.cleaned_data["tshirt_size"]


            MUD.save()
            return redirect('accounts:profile_home')

        else:
            return render(request, "accounts/edit_info.html", {"user_data_form": user_data_form, "more_user_data_form":more_user_data_form})

    else:
        new_user_data_form = EditProfileUserInfo(instance=request.user)
        if hasattr(request.user, 'moreuserdata'):
            new_more_user_data_form = EditProfileMoreUserDataInfo(instance=request.user.moreuserdata)

        else:
            new_more_user_data_form = EditProfileMoreUserDataInfo()

        return render(request, "accounts/edit_info.html", {"user_data_form": new_user_data_form, "more_user_data_form": new_more_user_data_form})


# QRgenerator(secret_string)

@login_required
@email_confirmation_required
def display_user_registered_events(request):
    event_set = request.user.moreuserdata.participating_events.all()
    return_event_set = list()
    for event in event_set:
        E = {"name": event.name}
        if str(event.logo):
            E["logo"] = event.logo.url

        return_event_set.append(E)
    return render(request, "accounts/myevents.html",
                  {"events": return_event_set, "default_logo": "/media/events/defaults/logo.png"})


@login_required
@email_confirmation_required
def register_user_for_event(request, event_name):
    try:
        event_name = str(event_name)
    except ValueError:
        return render(request, "accounts/invalid_request.html")

    if not hasattr(request.user, 'moreuserdata'):
        return render(request, "accounts/invalid_request.html", {
            "message": "Your Profile is missing some critical information. Please go to your profile and fill out the missing information before registering for the event",
            "links": ["incomplete_profile"]})

    event_name = event_name.lower().replace('-', ' ')
    if request.method == 'POST':
        register_form = EventRegisterForm(request.POST)

        if register_form.is_valid():
            if request.user.username == register_form.cleaned_data["username"]:
                if event_name == register_form.cleaned_data["event"]:
                    event = get_object_or_404(Event, name=event_name)
                    if request.user.moreuserdata in event.participants.all():
                        return render(request, "accounts/invalid_request.html",
                                      {"message": "You are already registered for this event"})
                    else:
                        event.participants.add(request.user.moreuserdata)
                else:
                    return render(request, "accounts/invalid_request.html", {"message": "Invalid request"})
            else:
                return render(request, "accounts/invalid_request.html", {"message": "Invalid request"})
        else:
            return render(request, "accounts/invalid_request.html", {"message": "Invalid request"})

        return render(request, "accounts/registration_complete.html",
                      {"username": register_form["username"].value(), "event": register_form['event'].value()})
    else:
        return render(request, "accounts/invalid_request.html", {"message": "Invalid request"})


@login_required
@email_confirmation_required
def un_register_user_for_event(request, event_name):
    event_slug = event_name
    try:
        event_name = str(event_name)
    except ValueError:
        return render(request, "accounts/invalid_request.html", {"message": "Invalid request"})

    if not hasattr(request.user, 'moreuserdata'):
        return render(request, "accounts/invalid_request.html", {"message": "Invalid request"})

    event_name = event_name.lower().replace('-', ' ')
    if request.method == 'POST':
        register_form = EventRegisterForm(request.POST)

        if register_form.is_valid():
            if request.user.username == register_form.cleaned_data["username"]:
                if event_name == register_form.cleaned_data["event"]:
                    event = get_object_or_404(Event, name=event_name)
                    if request.user.moreuserdata in event.participants.all():
                        event.participants.remove(request.user.moreuserdata)

                    else:
                        return render(request, "accounts/invalid_request.html",
                                      {"message": "You are anyway not participating in this event"})

                else:
                    return render(request, "accounts/invalid_request.html", {"message": "Invalid request"})
            else:
                return render(request, "accounts/invalid_request.html", {"message": "Invalid request"})
        else:
            return render(request, "accounts/invalid_request.html", {"message": "Invalid request"})

        return render(request, "accounts/un_registration_complete.html",
                      {"username": register_form["username"].value(), "event": register_form['event'].value(),
                       "event_slug": event_slug})
    else:
        return render(request, "accounts/invalid_request.html", {"message": "Invalid request"})


@login_required
@email_confirmation_required
def maps(request):
    return render(request, "accounts/map.html")


@login_required
@email_confirmation_required
def calender(request):
    return render(request, "accounts/calender.html")

