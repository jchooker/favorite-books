from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books', views.success),
    path('reg_attempt', views.reg_attempt),
    path('login_attempt', views.login_attempt),
    path('log_out', views.log_out),
]
