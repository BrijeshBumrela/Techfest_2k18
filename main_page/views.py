from django.shortcuts import render, redirect


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, "main_page/index.html", {"username": username})

    else:
        return render(request, "main_page/index.html")


def redirect_to_index(request):
    return redirect(to="/index")
