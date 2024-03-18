from django.shortcuts import render,HttpResponse
from .models import *

# Create your views here.
def index(request):
    return HttpResponse("THis is index page")


def listProduct(request):
    products = Laptop.objects.all()
    print(products)
    context = {'products':products}
    return render(request,"Laptop/index.html",context) 