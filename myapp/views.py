from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
import os

def index(request):
    return render(request,'index.html')

def admin_lense_add(request):
    return render(request,'admin_lenseadd.html')

def admin_lense_update(request):
    return render(request,'admin_lenseupdate.html')