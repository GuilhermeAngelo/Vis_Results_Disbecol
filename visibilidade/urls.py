# visibilidade/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboards:my")
    return redirect("account_login")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("uploads/", include("uploads.urls")),
    path("dashboard/", include("dashboards.urls")),
    path("", home, name="home"),
]