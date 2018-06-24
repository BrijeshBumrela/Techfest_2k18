from django.shortcuts import render, redirect, get_object_or_404

import data.models
import data.forms


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, "main_page/index.html", {"username": username})

    else:
        return render(request, "main_page/index.html")


def redirect_to_index(request):
    return redirect(to="/index")


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
    event_name = event_name.replace('-', ' ')
    event_name = event_name.lower()

    event = get_object_or_404(data.models.Event, name=event_name)
    event_organisers = event.organisers.all()
    logo = None
    if str(event.logo) != "" :
        logo = event.logo.url
    return render(request, "main_page/event_info.html", {"event": event, "organisers": event_organisers , "logo":logo})
