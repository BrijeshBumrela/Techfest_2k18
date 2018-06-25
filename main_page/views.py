from django.shortcuts import render, redirect


# Create your views here.

def index(request):
    return render(request, "main_page/index.html")


def redirect_to_index(request):
    return redirect(to="/index")
