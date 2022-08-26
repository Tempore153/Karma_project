from django.urls import path
from . import views

#liqpay
from django.urls import re_path
from accounts.views import PayView, PayCallbackView

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('donate/', views.donate, name="donate"),

    re_path(r'^pay/$', PayView.as_view(), name='pay_view'),
    re_path(r'^pay-callback/$', PayCallbackView.as_view(), name='pay_callback'),
    ]