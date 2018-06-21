from django.shortcuts import render, redirect
from data.models import MoreUserData
from django.contrib.auth.models import User
from registration.forms import MoreUserDataForm
from django.contrib.auth.decorators import login_required
import os.path




# Create your views here.

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

            MUD = MoreUserData(
                user=request.user,
                college_name=user_data_form.cleaned_data["college_name"],
                github_id=user_data_form.cleaned_data["github_id"],
                hackerrank_id=user_data_form.cleaned_data["hackerrank_id"],
                codechef_id=user_data_form.cleaned_data["codechef_id"],
                codeforces_id=user_data_form.cleaned_data["codeforces_id"]
            )
            if "profile_pic" in request.FILES:
                MUD.profile_pic = request.FILES["profile_pic"]

            MUD.save()
            return redirect('home')

        else:
            return render(request, "accounts/edit_additional_info.html", {"data_form": user_data_form})

    else:
        if hasattr(request.user, 'moreuserdata'):
            new_form = MoreUserDataForm(instance=request.user.moreuserdata)

        else:
            new_form = MoreUserDataForm()

        return render(request, "accounts/edit_additional_info.html", {"data_form": new_form})
