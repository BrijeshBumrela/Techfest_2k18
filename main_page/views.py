from django.shortcuts import render, redirect, get_object_or_404

import data.models
import data.forms
import datetime
import pytz
from .forms import EventRegisterForm

# Create your views here.

month_to_word = {1: "Janury",
                 2: "February",
                 3: "March",
                 4: "April",
                 5: "May",
                 6: "June",
                 7: "July",
                 8: "August",
                 9: "September",
                 10: "October",
                 11: "November",
                 12: "December"
                 }


def get_required_date_time_data(start_date, end_date,utc_start_date,utc_end_date):
    if not isinstance(start_date, datetime.datetime):
        raise ValueError("Received start-date is not an instance of datetime.datetime")

    if not isinstance(end_date, datetime.datetime):
        raise ValueError("Received end-date is not an instance of datetime.datetime")

    retmonth = month_to_word[start_date.month]
    retdate = start_date.day
    retdate = str(retdate)
    retdatesupscript = "th"
    if retdate[-1] == '1':
        retdatesupscript = "st"
    elif retdate[-1] == '2':
        retdatesupscript = "nd"
    elif retdate[-1] == '3':
        retdatesupscript = "rd"

    rettime_block = "AM"
    rethour = start_date.hour

    if start_date.hour > 12:
        rethour -= 12
        rettime_block = "PM"

    retmin = start_date.minute

    duration = utc_end_date - utc_start_date
    retdiffdays = duration.days
    diffsec = duration.seconds
    retdiffhours = diffsec // 3600
    diffsec -= (retdiffhours * 3600)
    retdiffminutes = diffsec // 60

    retfinaldiff = ""
    if retdiffdays:
        if retdiffdays == 1:
            retfinaldiff += str(retdiffdays) + " Day" + " "
        else:
            retfinaldiff += str(retdiffdays) + " Days" + " "
    if retdiffhours:
        retfinaldiff += str(retdiffhours) + " Hours" + " "

    if not retfinaldiff:
        retfinaldiff = str(retdiffminutes) + " Minutes"
    else:
        if retdiffminutes:
            retfinaldiff += str(retdiffminutes) + " Minutes"

    return {"month": retmonth,
            "date": retdate,
            "datesuperscript": retdatesupscript,
            "timeblock": rettime_block,
            "hour": rethour,
            "diff": retfinaldiff
            }


def index(request):
    render_dict = {}

    if request.user.is_authenticated:
        username = request.user.username
        render_dict["username"] = username

    events = list()
    for event in data.models.Event.objects.all():
        E = {"name": event.name.title()}
        if str(event.logo) :
            E["logo"] = event.logo.url
        if hasattr(event, 'eventcatalogue'):
            if str(event.eventcatalogue.image1):
                E["prime_image"] = event.eventcatalogue.image1.url

        localtimezone = pytz.timezone('Asia/Kolkata')
        local_start_date_time = event.start_date_time.astimezone(localtimezone)
        local_end_date_time = event.start_date_time.astimezone(localtimezone)
        E["calender"] = get_required_date_time_data(local_start_date_time, local_end_date_time, event.start_date_time,event.end_date_time)
        events.append(E)

    render_dict["events"] = events
    render_dict["event_coming_soon_image"] = '/media/events/defaults/coming_soon.jpg'
    render_dict["default_logo"] = '/media/events/defaults/logo.png'
    return render(request, "main_page/index.html", render_dict)


def redirect_to_index(request):
    return redirect('/index')


def display_events(request):
    events = list()
    for i in data.models.Event.objects.all():
        event = {"out_form": data.forms.BriefEventForm(instance=i)}
        if str(i.logo) == "":
            event["logo"] = None
        else:
            event["logo"] = i.logo.url

        events.append(event)

    return render(request, "main_page/events.html", {"events": events})


def event_info(request, event_name):
    event_name = event_name.lower()
    event_slug = event_name
    event_name = event_name.replace('-', ' ')


    event = get_object_or_404(data.models.Event, name=event_name)
    event_organisers = event.organisers.all()
    logo = None
    if str(event.logo) != "":
        logo = event.logo.url

    if request.user.is_authenticated :
        registerform = EventRegisterForm({"username":request.user.username,"event":event_name})
        return render(request, "main_page/temp_event_info.html", {"event": event, "organisers": event_organisers, "logo": logo, "authenticated": True, "registerform":registerform, "event_slug":event_slug})

    else :
        return render(request, "main_page/temp_event_info.html", {"event": event, "organisers": event_organisers, "logo": logo})
