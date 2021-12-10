from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('reg_attempt', views.reg_attempt),
    path('login_attempt', views.login_attempt),
    path('success', views.success),
    path('log_out', views.log_out),
]
