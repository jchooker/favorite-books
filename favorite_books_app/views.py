from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    context = {
    }
    return render(request, 'index.html', context)

def reg_attempt(request):
    context = {
    }
    return redirect('/')

def login_attempt(request):
    context = {
    }
    return render(request, 'index.html', context)

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user':user
    }
    return render(request, "success.html", context)

def log_out(request):
    request.session.flush()
    return redirect('/')