from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

# app_name = '1C'

urlpatterns = [
    path('check', CheckView.as_view(), name="check"),

    path(
        "check-list",
        login_required(CheckListView.as_view(template_name="OneC/check_list.html")),
        name="check-list",
    ),

    path(
        "create-check",
        login_required(CreateCheckView.as_view(template_name="OneC/create_check.html")),
        name="create-check",
    ),

    path("get_orders_from_clients_and_dates", get_orders_from_clients_and_dates,
         name="get_orders_from_clients_and_dates"),

    path("generate_check", generate_check, name="generate_check"),


]
