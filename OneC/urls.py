from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *


app_name = 'oneC'
urlpatterns = [
    path('check', CheckView.as_view(), name="check"),
]
