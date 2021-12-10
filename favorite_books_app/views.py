from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def reg_attempt(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST) 
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="reg")
        temp_pw = request.POST["pw"]
        pw_hash = bcrypt.hashpw(temp_pw.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        pw = pw_hash
        )
        return redirect('/success')
    else:
        return redirect('/')

def login_attempt(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
    context = {
    }
    return redirect('/success')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user':user
    }
    return render(request, "user_landing.html", context)

def log_out(request):
    request.session.flush()
    return redirect('/')