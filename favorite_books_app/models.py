from django.db import models


# class UserManager(models.Manager):
#     def user_validator(self, postData):
#         pass
#     def book_validator(self, postData):
#         pass

class User(models.Model):
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    email = models.EmailField(max_length = 40)
    pw = models.CharField(max_length = 40)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)

class Book(models.Model):
    title = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
