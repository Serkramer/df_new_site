from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *


urlpatterns = [
    path('check', CheckView.as_view(), name="check"),

    path(
        "check-list",
        login_required(CheckListView.as_view(template_name="OneC/check_list.html")),
        name="check-list",
    ),
]
