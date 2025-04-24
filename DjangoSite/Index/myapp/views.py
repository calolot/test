import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "Main.html")
def consultportal(request):
    return render(request, "ConsultationPortal.html")