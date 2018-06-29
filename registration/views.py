from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from data.tokens import account_activation_token


# Create your views here.


def send_account_activation_email(request, user_instance):
    current_site = get_current_site(request)
    email_subject = "Activate Your Technobots2k18 Account "
    email_message = render_to_string('data/account_activation_email_template.html',
                                     {'user_fullname': user_instance.get_full_name(),
                                      'domain': current_site.domain,
                                      'uid': urlsafe_base64_encode(
                                          force_bytes(
                                              user_instance.pk)),
                                      'token': account_activation_token.make_token(
                                          user_instance),
                                      })

    user_instance.email_user(email_subject, email_message)

    return

    # return redirect('registration:account_activation_email_sent')


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
            # user_instance = new_user
            send_account_activation_email(request, new_user)


            # login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('registration:account_activation_email_sent')

        else:
            return render(request, 'registration/signup.html', {"signup_form": new_user_form})

    else:
        new_form = forms.UserForm()
        return render(request, 'registration/signup.html', {"signup_form": new_form})


def logout_view(request):
    logout(request)
    return redirect('home')


def account_activation_email_sent(request):
    return render(request, "registration/account_activation_email_sent.html")
