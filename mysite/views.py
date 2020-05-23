import datetime
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse
# from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_data
from blog.models import Blog


def home(request):
    context = {}
    return render(request, "home.html", context)
