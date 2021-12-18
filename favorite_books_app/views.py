from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from time import localtime, strftime
from datetime import datetime

# Create your views here.
def curr_user(request):
    return User.objects.get(id=request.session['user_id'])

def curr_book(request, book_id):
    return Book.objects.get(id=book_id)

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
    print("NEW TEST")
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="log")
            return redirect('/')
        user = User.objects.get(email=request.POST['email2'])
        request.session['user_id'] = user.id
        print(request.session['user_id'])
        # request.session['']
    else:
        return redirect('/')
    return redirect('/books')

def success(request):
    if 'user_id' not in request.session:
        messages.error(request, "TEST")
        return redirect('/')
    # user = User.objects.get(id=request.session['user_id'])
    # books = user.books_uploaded.all()
    context = {
        'user':curr_user(request),
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
        user = curr_user(request)
        book = Book.objects.create(
        title = request.POST['title'],
        desc = request.POST['desc'],
        uploaded_by = user
        )
        book.users_who_like.add(user)
        # request.session['book_id'] = book.id
        return redirect(f'/books/{book.id}')
    else:
        return redirect('/books')

def book_info(request, book_id):
    book = curr_book(request, book_id)
    user = curr_user(request)
    cr_at = book.created_at.strftime("%b %d, %Y: %H:%M %p")
    up_at = book.updated_at.strftime("%b %d, %Y: %H:%M %p")
    context = {
        'book': book,
        'user': user,
        'created_at': cr_at,
        'updated_at': up_at
    }
    if book.uploaded_by.id == request.session['user_id']:
        return render(request, "book_info_admin.html", context)
    return render(request, "book_info.html", context)

def update(request, book_id):
    book = curr_book(request, book_id)
    book.title = request.POST['re_title']
    book.desc = request.POST['re_desc']
    book.save()
    return redirect(f'/books/{book_id}')

def favorite(request, book_id):
    user = curr_user(request)
    book = curr_book(request, book_id)
    user.favorited_books.add(book)

    return redirect(f'/books/{book_id}')

def unfavorite(request, book_id):
    user = curr_user(request)
    book = curr_book(request, book_id)
    user.favorited_books.remove(book)

    return redirect(f'/books/{book_id}')

def log_out(request):
    request.session.flush()
    return redirect('/')