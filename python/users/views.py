from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from users.forms import RegistrationForm, LoginForm


@login_required
def index(request):
    return render(request, "users/dashboard.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect('users:guest')


def guest(request):
    login_form = LoginForm(data=request.POST or None, prefix="login")
    register_form = RegistrationForm(data=request.POST or None, prefix="register")
    if request.POST:
        import pdb
        pdb.set_trace()
        if login_form.is_valid():
            user = login_form.login()
            if user.is_active:
                login(request, user)
                return redirect('users:index')
            else:
                messages.error(request, 'This account has been deleted.')
                return redirect('users:guest')
        elif register_form.is_valid():
            user = register_form.save()
            # FIXME change to validation email later
            login(request, user)
            return redirect('users:index')

    return render(request, "users/guest.html", {"login_form": login_form, "register_form": register_form})
