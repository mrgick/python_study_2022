from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm


def registration(request, next_page='/'):
    if request.user.is_authenticated:
        return redirect(next_page)
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(next_page)
    else:
        form = SignUpForm()
    return render(request, "accounts/registration.html", {'form': form})
