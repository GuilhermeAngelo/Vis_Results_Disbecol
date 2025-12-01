from django.urls import path
from . import views

app_name = "uploads"

urlpatterns = [
    # /uploads/  -> formulário e POST
    path("", views.upload_csv, name="upload"),
]
