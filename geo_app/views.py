from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from datetime import datetime


def home(request):

    """Main Driver Function for User data visualization and filtering with necessary information."""

    context = {}
    return render(request, 'home.html', context)


def get_details(request):

    """This Function will return the Project details along with location data in a viewable format."""
    return

