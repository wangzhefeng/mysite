from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from .forms import LoginForm, RegForm


def login(request):
    # method 1
    # username = request.POST.get("username", "")
    # password = request.POST.get("password", "")
    # user = auth.authenticate(request, username = username, password = password)
    # referer = request.META.get("HTTP_REFERER", reverse("home"))
    # if user is not None:
    #     auth.login(request, user)
    #     # Redirect to a success page.
    #     return redirect(referer)
    # else:
    #     # Return an 'invalid login' error message.
    #     return render(request, "error.html", {"message": "用户名或密码不正确"})
    
    # method 2: django form
    if request.method == "POST": 
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data["user"]
            auth.login(request, user)

            return redirect(request.GET.get("from", reverse("home")))
    else:
        login_form = LoginForm()

    context = {}
    context["login_form"] = login_form

    return render(request, "user/login.html", context)


def register(request):
    if request.method == "POST": 
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data["username"]
            email = reg_form.cleaned_data["email"]
            password = reg_form.cleaned_data["password"]
            # 创建用户 method 1
            user = User.objects.create_user(username, email, password)
            user.save()
            # 创建用户 method 2
            # user = User()
            # user.username = username
            # user.email = email
            # user.set_password(password)
            # user.save()
            # 登陆用户
            user = user.auth.authenticate(username = username, password = password)
            auth.login(request, user)
            return redirect(request.GET.get("from", reverse("home")))
    else:
        reg_form = RegForm()

    context = {}
    context["reg_form"] = reg_form
    return render(request, "user/register.html", context)


def logout(request):
    auth.logout(request)

    return redirect(request.GET.get("from", reverse("home")))


def user_info(request):
    context = {}
    
    return render(request, "user/user_info.html", context)
