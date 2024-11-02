from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'map'
urlpatterns = [

    path('post-office-autocomplete/', login_required(views.PostOfficeAutocomplete.as_view()),
         name='post-office-autocomplete'),
    path('settlements-autocomplete/', login_required(views.SettlementsAutocomplete.as_view()),
         name='settlements-autocomplete'),
    path('areas-autocomplete/', login_required(views.AreasAutocomplete.as_view()), name='areas-autocomplete'),

]
