import stripe
import logging
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.generic import View,TemplateView
from django.http import JsonResponse
from .models import *
from secondapp.models import User_Data
from django.core.paginator import Paginator,PageNotAnInteger
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.decorators import method_decorator


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

def redirect_to_login(request):
    return redirect('accounts/login') 

class SuccessView(TemplateView):
    template_name = "laptop/success.html"

@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        print(f"this is request dictionary {request}")
        YOUR_DOMAIN = 'http://127.0.0.1:8000/'  # Adjust this URL as needed
        p_id = kwargs.get('id')
        user = request.user
        try:
            product = Laptop.objects.get(id = p_id)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data':{
                            'currency':'usd',
                            'unit_amount':product.price * 100,
                            'product_data':{
                                'name':product.name,
                                'images':[product.main_img],
                            }
                        },
                        'quantity':1,
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        # 'price': "price_1PGKQBHdyG3oyik5wzb6ml6J",
                        # 'quantity': 1,
                    },
                ],
                metadata={
                    'product_id':product.id,
                    'user_id':user.id
                },
                mode='payment',
                success_url=YOUR_DOMAIN + 'success/',
                cancel_url=YOUR_DOMAIN + 'cancel.html',
                automatic_tax={'enabled': True},
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        # Redirect to the checkout session URL
        return redirect(checkout_session.url, status=303)
    
    
logger = logging.getLogger(__name__)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session_id = event['data']['object']['id']
        try:
            session = stripe.checkout.Session.retrieve(
                session_id,
                expand=['line_items'],
            )
            logger.info(f"Session retrieved: {session_id}")

            customer_email = session['customer_details']['email']
            product_id = session['metadata'].get('product_id')
            user_id = session['metadata'].get('user_id')

            if not product_id or not user_id:
                logger.error(f"Missing product_id or user_id in session metadata: {session['metadata']}")
                return HttpResponse(status=400)

            fulfill_order(user_id, product_id)

            product = Laptop.objects.get(id=product_id)
            send_mail(
                subject=f'Here is your product {product.name}',
                message='Thanks for buying this product',
                recipient_list=[customer_email],
                from_email="matt@test.com",
            )

            line_items = session.line_items
            logger.info(f"Line items: {line_items}")
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            return HttpResponse(status=400)
        except Laptop.DoesNotExist:
            logger.error(f"Laptop not found: {product_id}")
            return HttpResponse(status=400)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=200)

def fulfill_order(user_id, p_id):
    try:
        product = Laptop.objects.get(id=p_id)
        us = User_Data.objects.get(id=user_id)

        ord = order.objects.create(
            product=product,
            user=us,
            quantity=1,
            total_price=product.price
        )
        ord.save()
        logger.info(f"Order fulfilled for user: {user_id}, product: {p_id}")
    except Laptop.DoesNotExist:
        logger.error(f"Laptop not found: {p_id}")
        raise
    except User_Data.DoesNotExist:
        logger.error(f"User not found: {user_id}")
        raise
    except Exception as e:
        logger.error(f"Error fulfilling order: {e}")
        raise
     
  

def listProduct(request):
    products = Laptop.objects.all()
    pro_line = product_line.objects.all()
    
    paginated = Paginator(products,2)  #This is the paginator class which Django used for pagination 
    page_number = request.GET.get('page')
    
    try:
        products  = paginated.get_page(page_number)
    except PageNotAnInteger:
        products  = paginated.page(1)  #this will assign first page to page_obj if the page is not an integer
        
    return render(request, 'Laptop/index.html' , {'products' : products,'pro_line':pro_line })

def load_more_products(request):
    products = Laptop.objects.all()
    paginated = Paginator(products,2)
    print(paginated)
    page_number = request.GET.get('page')
    print(page_number)
    
    try:
        products_page = paginated.get_page(page_number)
        print(products_page)
    except PageNotAnInteger:
        products_page = paginated.page(1)
    
    html_content = render_to_string('Laptop/partial_data.html', {'products': products_page})
    print(products)
    # print(html_content)
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
