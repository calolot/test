from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "Main"),
    path("ConsultationPortal/", views.consultportal, name = "ConsultationPortal"),
]