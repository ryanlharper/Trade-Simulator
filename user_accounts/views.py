from django.shortcuts import render
from django.http import HttpResponse
from .utils import update_values

def update(request):
    update_values()
    return HttpResponse("Values updated successfully")