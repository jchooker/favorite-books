from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books', views.success),
    path('reg_attempt', views.reg_attempt),
    path('login_attempt', views.login_attempt),
    path('add_book', views.add_book),
    path('books/<int:book_id>', views.book_info),
    path('books/<int:book_id>/update', views.update),
    path('books/<int:book_id>/delete', views.delete),
    path('log_out', views.log_out),
]
