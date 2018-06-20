from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import login,logout


# Create your views here.

def signup(request):
    if request.method == "POST":
        new_user_form = forms.UserForm(request.POST)

        if new_user_form.is_valid():
            new_user = User.objects.create_user(
                username=new_user_form.cleaned_data["username"],
                password=new_user_form.cleaned_data["password"],
                email=new_user_form.cleaned_data["email"]
            )

            new_user.first_name = new_user_form.cleaned_data["first_name"]
            new_user.last_name = new_user_form.cleaned_data["last_name"]
            new_user.save()

            login(request,new_user)
            return redirect(to="home")

        else:
            return render(request, 'registration/signup.html', {"signup_form": new_user_form})

    else:
        new_form = forms.UserForm()
        return render(request, 'registration/signup.html', {"signup_form": new_form})


def logout_view(request):
    logout(request)
    return redirect('home')
