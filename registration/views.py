from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from data.tokens import account_activation_token
from django.contrib.auth.decorators import login_required

from django.db import connection
from data.async import run_in_background


@run_in_background
def send_account_activation_email(request, user_instance):
    current_site = get_current_site(request)
    email_subject = "Activate Your Technobots2k18 Account "
    email_message = render_to_string('data/account_activation_email_template.html',
                                     {'user_fullname': user_instance.get_full_name(),
                                      'domain': current_site.domain,
                                      'uid': urlsafe_base64_encode(
                                          force_bytes(
                                              user_instance.pk)).decode(),
                                      'token': account_activation_token.make_token(
                                          user_instance),
                                      })

    user_instance.email_user(email_subject, email_message)
    connection.close()
    return

    # return redirect('registration:account_activation_email_sent')

@run_in_background
def send_welcome_mail(user_instance):
    """
    Sends a welcome and confirmation mail after account has been activated
    """
    email_subject = "Welcome to Technobots2k18 "
    email_message = render_to_string('registration/welcome.html',
                                     {'user_fullname': user_instance.get_full_name(),
                                      })

    user_instance.email_user(email_subject, email_message)
    connection.close()
    return


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


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.emailconfirmation.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        send_welcome_mail(user)
        return redirect('home')

    elif user is None:
        return render(request, 'registration/invalid_activation_link.html', {"isnone": True})
    else:
        return render(request, 'registration/invalid_activation_link.html')


@login_required
def generate_new_activation_link(request):
    send_account_activation_email(request, request.user)
    return redirect('registration:account_activation_email_sent')
