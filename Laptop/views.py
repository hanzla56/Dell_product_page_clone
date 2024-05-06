from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.template.loader import render_to_string


# Create your views here.
def index(request):
    return HttpResponse("THis is index page")


# def listProduct(request):
#     products = Laptop.objects.all()
#     print(products)
#     pro_line = product_line.objects.all()
#     print(pro_line)
#     context = {
#                'products':products,
#                'pro_line':pro_line
#                }
#     return render(request,"Laptop/index.html",context) 

def listProduct(request):
    products = Laptop.objects.all()
    pro_line = product_line.objects.all()
    
    paginated = Paginator(products,3)  #This is the paginator class which Django used for pagination 
    page_number = request.GET.get('page')
    
    try:
        products  = paginated.get_page(page_number)
    except PageNotAnInteger:
        products  = paginated.page(1)  #this will assign first page to page_obj if the page is not an integer
        
    return render(request, 'Laptop/index.html' , {'products' : products,'pro_line':pro_line })

def load_more_products(request):
    products = Laptop.objects.all()
    paginated = Paginator(products, 3)
    print(paginated)
    page_number = request.GET.get('page')
    print(page_number)
    
    try:
        products_page = paginated.get_page(page_number)
    except PageNotAnInteger:
        products_page = paginated.page(1)
    
    html_content = render_to_string('Laptop/partial_data.html', {'products': products})
    print(html_content)
    return JsonResponse({'html': html_content, 'has_next': products_page.has_next()})


def filter_data(request):
    if request.method == "GET":
        query_set = Laptop.objects.all()
        
        # Extract values for filtering
        product_lines = request.GET.getlist('product_line')
        print(product_lines)
        displays = request.GET.getlist('display')
        print(displays)

        if product_lines:
            query_set = query_set.filter(product_line__in=product_lines)
        
        if displays:
            query_set = query_set.filter(display__in=displays)

        data = []
        for laptop in query_set:
            laptop_data = {
                'id': laptop.id,
                'name': laptop.name,
                'model': laptop.model,
                'price': laptop.price,
                'short_processor_details': laptop.short_processor_details,
                'full_processor_details': laptop.full_processor_details,
                'graphics': laptop.graphics,
                'os': laptop.os,
                'memory': laptop.memory,
                'display': laptop.display,
                'img': laptop.main_img.url,
                'image_urls': [image.image.url for image in laptop.p_image.all()]
            }
            data.append(laptop_data)

        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error': 'invalid request'})




def product_detail(request,product_id):
    if request.method == "GET":
        s_product = Laptop.objects.get(id=product_id)
        return render(request,"Laptop/Detail.html",{'s_product':s_product})
    
def update_view(request,product_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        print(name)
        price = request.POST.get('price')
        print(price)
        memory = request.POST.get('memory')
        os = request.POST.get('os')
        processor = request.POST.get('processor')
        
        product = Laptop.objects.get(pk=product_id)
        if product:
            if name:
                product.name = name
            if price:
                product.price = price
            if memory:
                product.memory = memory
            if os:
                product.os = os
            if processor:
                product.full_processor_details = processor
                
        product.save()
        
        laptop_data={
            'id':product.id,
            'name':product.name,
            'price':product.price,
            'os':product.os,
            'processor':product.full_processor_details
        }
        print('data has been updated')
        
        return JsonResponse({'code':laptop_data})
            

        
