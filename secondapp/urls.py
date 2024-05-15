from django.contrib import admin
from django.urls import path,include
from secondapp import views

app_name = 'secondapp'

urlpatterns = [
    path("signup/",views.signup,name='signup')
]
