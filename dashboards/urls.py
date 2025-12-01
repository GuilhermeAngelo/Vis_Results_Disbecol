# dashboards/urls.py
from django.urls import path
from . import views

app_name = "dashboards"

urlpatterns = [
    path("me/", views.my_dashboard, name="my"),
]