from django.contrib import admin
from django.urls import path
from Laptop import views

app_name = "Laptop"


urlpatterns = [
    path("", views.listProduct,name='startpage'),
]
