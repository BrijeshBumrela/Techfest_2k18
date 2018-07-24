import datetime

import pytz
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from data.models import MoreUserData, Event
from django.contrib.auth.models import User
from data.forms import EditProfileMoreUserDataInfo, EditProfileUserInfo, ChangePasswordForm
from django.contrib.auth.decorators import login_required
from main_page.forms import EventRegisterForm
from django.contrib.auth import login
import os.path
# For encryption
import hashlib
# The QR code file
from . import QRcode

# Create your views here.


secret_string = ''
# QRgenerator(secret_string)

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


def get_user_details(request):
    user_details = {"username": request.user.username,
                    "fullname": request.user.get_full_name(),
                    }

    if hasattr(request.user, 'moreuserdata'):

        S = str(request.user.moreuserdata.profile_pic)
        if S is not '':
            user_details["profile_pic"] = request.user.moreuserdata.profile_pic.url
        else:
            user_details["profile_pic"] = '/media/profile_pictures/default/blank.jpg'
    else:
        user_details["profile_pic"] = '/media/profile_pictures/default/blank.jpg'

    return user_details


@login_required
@email_confirmation_required
def profile_home(request):
    user_details = get_user_details(request)
    if hasattr(request.user,"moreuserdata") :
        user_details["details_check"] = True
        MUD = request.user.moreuserdata
        user_details["about"] = MUD.description
        user_details["college"] = MUD.college_name
        user_details["email"] = request.user.email
        user_details["phone_number"] = str(MUD.country_code) + ' ' + str(MUD.phone_number)
        user_details["github_id"] = MUD.github_id
        user_details["hackerrank_id"] = MUD.hackerrank_id
        user_details["codechef_id"] = MUD.codechef_id
        user_details["codeforces_id"] = MUD.codeforces_id

    return render(request, "accounts/profile_home.html", {"active_profile": True, "profile": user_details})


@login_required
@email_confirmation_required
def edit_info(request):
    current_user_details = get_user_details(request)
    current_user_details["is_profile_pic_set"] = True
    if current_user_details["profile_pic"] == '/media/profile_pictures/default/blank.jpg':
        current_user_details["is_profile_pic_set"] = False
        current_user_details["edit_profile_pic"] = '/media/profile_pictures/default/add_pic.jpeg'
    if request.method == "POST":

        user_data_form = EditProfileUserInfo(request.POST)
        more_user_data_form = EditProfileMoreUserDataInfo(request.POST, request.FILES)

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

            if "profile_pic" in request.FILES:
                MUD.profile_pic = request.FILES["profile_pic"]

            MUD.save()
            return redirect('accounts:profile_home')

        else:
            return render(request, "accounts/edit_info.html",
                          {"user_data_form": user_data_form,
                           "more_user_data_form": more_user_data_form,
                           "profile": current_user_details,
                           })

    else:
        new_user_data_form = EditProfileUserInfo(instance=request.user)
        if hasattr(request.user, 'moreuserdata'):
            new_more_user_data_form = EditProfileMoreUserDataInfo(instance=request.user.moreuserdata)

        else:
            new_more_user_data_form = EditProfileMoreUserDataInfo()

        return render(request, "accounts/edit_info.html",
                      {"user_data_form": new_user_data_form,
                       "more_user_data_form": new_more_user_data_form,
                       "profile": current_user_details,
                       })




@login_required
@email_confirmation_required
def display_user_registered_events(request):
    user_details = get_user_details(request)
    event_set = request.user.moreuserdata.participating_events.all()
    return_event_set = list()
    localtimezone = pytz.timezone('Asia/Kolkata')
    cur_datetime = datetime.datetime.now().astimezone(localtimezone)
    for event in event_set:
        E = {"name": event.name.title(), }
        if event.start_date_time > cur_datetime:
            diff = event.start_date_time - cur_datetime
            if diff.days > 0:
                E["start_diff"] = "Starts In " + str(diff.days) + " Days"
            else:
                E["start_diff"] = "Starts In " + str(diff.seconds) + " Seconds"
        elif event.end_date_time > cur_datetime:
            diff = event.end_date_time - cur_datetime
            if diff.days > 0:
                E["end_diff"] = "Ends In " + str(diff.days) + " Days"
            else:
                E["end_diff"] = "Ends In " + str(diff.seconds) + " Seconds"

        if str(event.logo) is not "":
            E["logo"] = event.logo.url

        return_event_set.append(E)
    return render(request, "accounts/myevents.html",
                  {"profile": user_details,
                   "active_events": True,
                   "events": return_event_set,
                   "default_logo": "/media/events/defaults/logo.png"
                   }
                  )


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
def updates(request):
    user_details = get_user_details(request)
    return render(request, "accounts/updates.html", {"active_updates": True, "profile":user_details})

@login_required
@email_confirmation_required
def change_password(request):
    user_details = get_user_details(request)
    if request.method == "POST":
        password_form = ChangePasswordForm(request.POST)
        if password_form.is_valid():
            if not request.user.check_password(password_form.cleaned_data["old_password"]):
                password_form.errors["old_password"] = "Incorrect Current Password"
                return render(request, "accounts/change_password.html",
                              {"profile": user_details, "form": password_form,})
            elif password_form.cleaned_data["new_password"]!=password_form.cleaned_data["confirm_new_password"]:
                password_form.errors["confirm_new_password"] = "Both Passwords Do Not Match"
                return render(request, "accounts/change_password.html",
                              {"profile": user_details, "form": password_form, })
            else:
                request.user.set_password(password_form.cleaned_data["new_password"])
                request.user.save()
                login(request, request.user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('accounts:profile_home')

        else:
            return render(request, "accounts/change_password.html", {"profile": user_details, "form": password_form})

    else:
        password_form = ChangePasswordForm()
        return render(request, "accounts/change_password.html", {"profile": user_details,"form":password_form})


@login_required
@email_confirmation_required
def maps(request):
    return render(request, "accounts/map.html")


@login_required
@email_confirmation_required
def calender(request):
    return render(request, "accounts/calender.html")
