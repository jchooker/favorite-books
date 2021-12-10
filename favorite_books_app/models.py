import bcrypt
from django.db import models
import re


class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name_length'] = "Please provide a valid first name (two characters or more)"
        if len(postData['last_name']) < 2:
            errors['last_name_length'] = "Please provide a valid last name (two characters or more)"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = "Invalid email address!"
        if postData['pw_conf'] != postData['pw']:
            errors['pw_conf_match'] = "Confirmation password and password must match!"
    def login_validator(self, postData):
        errors = {}
        user_test = User.objects.filter(email = postData['email2'])
        if user_test:
            if not bcrypt.checkpw(postData['pw2'].encode(), user_test[0].pw.encode()):
                errors['bad_pw'] = "Bad email-password combination"
        else:
            errors['no_such_user'] = "Bad email-password combination"
    def book_validator(self, postData):
        pass

class User(models.Model):
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    email = models.EmailField(max_length = 40)
    pw = models.CharField(max_length = 40)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)

class Book(models.Model):
    title = models.CharField(max_length = 100)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded")
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
