from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.urls import reverse

def home(request):
    context = {}
    return render(request, "home.html", context)


def login(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = auth.authenticate(request, username = username, password = password)
    referer = request.META.get("HTTP_REFERER", reverse("home"))
    if user is not None:
        auth.login(request, user)
        # Redirect to a success page.
        return redirect(referer)
    else:
        # Return an 'invalid login' error message.
        return render(request, "error.html", {"message": "用户名或密码不正确"})