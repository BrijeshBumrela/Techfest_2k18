from django.shortcuts import render, redirect, get_object_or_404

import data.models
import data.forms
import data.defaults
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


def get_required_date_time_data(start_date, end_date, utc_start_date, utc_end_date):
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
    retmin = start_date.minute

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
            "minute": retmin,
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
        if str(event.logo):
            E["logo"] = event.logo.url
        if hasattr(event, 'eventcatalogue'):
            if str(event.eventcatalogue.image1):
                E["prime_image"] = event.eventcatalogue.image1.url

        localtimezone = pytz.timezone('Asia/Kolkata')
        local_start_date_time = event.start_date_time.astimezone(localtimezone)
        local_end_date_time = event.start_date_time.astimezone(localtimezone)
        E["calender"] = get_required_date_time_data(local_start_date_time, local_end_date_time, event.start_date_time,
                                                    event.end_date_time)
        events.append(E)

    render_dict["events"] = events
    render_dict["event_coming_soon_image"] = '/media/events/defaults/coming_soon.jpg'
    render_dict["default_logo"] = '/media/events/defaults/logo.png'
    return render(request, "main_page/index.html", render_dict)


def redirect_to_index(request):
    return redirect('/index')


def display_events(request):
    catagories = [c.name for c in data.models.EventCatagory.objects.all()]
    events = list()
    for i in data.models.Event.objects.all():
        event = dict()
        event["name"] = i.name.title()
        event["catagories"] = [xx.name for xx in i.catagories.all()]
        if str(i.logo) is "":
            event["logo"] = data.defaults.event_logo
        else:
            event["logo"] = i.logo.url

        events.append(event)

    return render(request, "main_page/events.html", {"events": events, "catagories": catagories})


def event_info(request, event_name):
    event_info_page = 'main_page/K_event_info.html'
    event_name = event_name.lower()
    event_slug = event_name
    event_name = event_name.replace('-', ' ')

    event = get_object_or_404(data.models.Event, name=event_name)
    event_duration = event.end_date_time - event.start_date_time
    event_duration_string = ""
    if event_duration.days > 0:
        event_duration_string += " " + str(event_duration.days) + " Days"
    if event_duration.seconds//3600 > 0:
        event_duration_string += " " + str(event_duration.seconds//3600) + " Hours"
    if (event_duration.seconds % 3600)//60 > 0:
        event_duration_string += " " + str((event_duration.seconds % 3600)//60) + " Minutes"

    event_organisers = event.organisers.all()
    event_logo = data.defaults.event_logo
    if str(event.logo):
        event_logo = event.logo.url

    event_catalogue = list()
    if hasattr(event, 'eventcatalogue'):
        if event.eventcatalogue.image1.name:
            event_catalogue.append(event.eventcatalogue.image1.url)

            if event.eventcatalogue.image2.name:
                event_catalogue.append(event.eventcatalogue.image2.url)

                if event.eventcatalogue.image3.name:
                    event_catalogue.append(event.eventcatalogue.image3.url)

                    if event.eventcatalogue.image4.name:
                        event_catalogue.append(event.eventcatalogue.image4.url)

                        if event.eventcatalogue.image5.name:
                            event_catalogue.append(event.eventcatalogue.image5.url)

                            if event.eventcatalogue.image6.name:
                                event_catalogue.append(event.eventcatalogue.image6.url)

        else:
            event_catalogue.append(data.defaults.event_prime_catalogue)
    else:
        event_catalogue.append(data.defaults.event_prime_catalogue)

    if request.user.is_authenticated:
        registerform = EventRegisterForm({"username": request.user.username, "event": event_name})
        if hasattr(request.user, "moreuserdata"):
            if event.participants.all().filter(pk=request.user.moreuserdata.user_id).exists():
                return render(request, event_info_page,
                              {"event": event, "organisers": event_organisers, "logo": event_logo,
                               "catalogue": event_catalogue,
                               "duration": event_duration_string,
                               "authenticated": True,
                               "registerform": registerform, "event_slug": event_slug, "registered": True})

            else:
                return render(request, event_info_page,
                              {"event": event, "organisers": event_organisers, "logo": event_logo,
                               "catalogue": event_catalogue,
                               "duration": event_duration_string,
                               "authenticated": True,
                               "registerform": registerform, "event_slug": event_slug, "registered": False})

        return render(request, event_info_page,
                      {"event": event, "organisers": event_organisers, "logo": event_logo,
                       "catalogue": event_catalogue,
                       "duration": event_duration_string,
                       "authenticated": True,
                       "registerform": registerform, "event_slug": event_slug})

    else:
        return render(request, event_info_page,
                      {"event": event, "organisers": event_organisers,
                       "logo": event_logo,
                       "duration": event_duration_string,
                       "catalogue": event_catalogue,
                       })


def contact_us(request):
    return render(request, "main_page/contact_us.html")


def temp_event_info(request):
    return render(request, "main_page/event_info.html")
