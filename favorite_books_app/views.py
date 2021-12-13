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
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="reg")
            return redirect('/')
        temp_pw = request.POST["pw"]
        pw_hash = bcrypt.hashpw(temp_pw.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        pw = pw_hash
        )
        request.session['user_id']=User.objects.last().id
        return redirect('/books')
    else:
        return redirect('/')

def login_attempt(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="log")
            return redirect('/')
        user = User.objects.get(email=request.POST['email2'])
        request.session['user_id'] = user.id
        # request.session['']
    else:
        return redirect('/')
    return redirect('/books')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    # user = User.objects.get(id=request.session['user_id'])
    # books = user.books_uploaded.all()
    context = {
        'user':User.objects.get(id=request.session['user_id']),
        'books':Book.objects.all()
    }
    return render(request, "user_landing.html", context)

def add_book(request):
    if request.method == 'POST':
        errors = Book.objects.book_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        # book = Book.objects.get(title=request.POST['title'])
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(
        title = request.POST['title'],
        desc = request.POST['desc'],
        uploaded_by = user
        )
        book.users_who_like.add(user)
        # request.session['book_id'] = book.id
        return redirect(f'/books/{id}')
    else:
        return redirect('/books')

def book_info(request, book_id):
    context = {
        'book':Book.objects.get(id=book_id),
        'users':User.objects.all()
    }
    return render(request, "book_info.html", context)

def favorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.favorited_books.add(book)

    return redirect(f'/books/{book_id}')

def unfavorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.favorited_books.remove(book)

    return redirect(f'/books/{book_id}')

def log_out(request):
    request.session.flush()
    return redirect('/')