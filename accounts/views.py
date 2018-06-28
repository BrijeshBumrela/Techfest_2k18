from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from data.models import MoreUserData, Event
from django.contrib.auth.models import User
from registration.forms import MoreUserDataForm
from django.contrib.auth.decorators import login_required
from main_page.forms import EventRegisterForm
import os.path
# For encryption
import hashlib
# The QR code file
from . import QRcode

# Create your views here.


string = ''


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
def edit_additional_info(request):
    if request.method == "POST":

        user_data_form = MoreUserDataForm(request.POST, request.FILES)
        if user_data_form.is_valid():

            MUD = None
            if hasattr(request.user, 'moreuserdata'):
                MUD = request.user.moreuserdata
            else:
                MUD = MoreUserData()
                MUD.user = request.user
                # Encryption
                MUD.secret_key = MD5encrypt(request.user.username)
                # Using the variable string to send to qrcode
                string = str(MUD.secret_key)

            MUD.college_name = user_data_form.cleaned_data["college_name"]
            MUD.github_id = user_data_form.cleaned_data["github_id"]
            MUD.hackerrank_id = user_data_form.cleaned_data["hackerrank_id"]
            MUD.codechef_id = user_data_form.cleaned_data["codechef_id"]
            MUD.codeforces_id = user_data_form.cleaned_data["codeforces_id"]
            MUD.description = user_data_form.cleaned_data["description"]

            if "profile_pic" in request.FILES:
                MUD.profile_pic = request.FILES["profile_pic"]

            MUD.save()
            return redirect('accounts:profile_home')

        else:
            return render(request, "accounts/edit_additional_info.html", {"data_form": user_data_form})

    else:
        if hasattr(request.user, 'moreuserdata'):
            new_form = MoreUserDataForm(instance=request.user.moreuserdata)

        else:
            new_form = MoreUserDataForm()

        return render(request, "accounts/edit_additional_info.html", {"data_form": new_form})


# QRgenerator(string)


@login_required
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
                      {"username": register_form["username"].value(), "event": register_form['event'].value(),"event_slug":event_slug})
    else:
        return render(request, "accounts/invalid_request.html", {"message": "Invalid request"})
